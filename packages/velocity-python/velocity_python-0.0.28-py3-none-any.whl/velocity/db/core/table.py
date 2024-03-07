from velocity.db import exceptions
from velocity.db.core.row import Row
from velocity.db.core.result import Result
from velocity.db.core.column import Column
from velocity.db.core.decorators import (
    return_default,
    create_missing,
    reset_id_on_dup_key,
)


class Query(str):
    pass


class Table(object):
    def __init__(self, tx, name):
        self.tx = tx
        assert self.tx
        self.name = name.lower()
        assert self.name
        self.sql = tx.engine.sql
        assert self.sql

    def __str__(self):
        return """
    Table: %s
    (table exists) %s
    Columns: %s
    Rows: %s
        """ % (
            self.name,
            self.exists(),
            len(self.columns),
            len(self),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.close()

    def close(self):
        try:
            self._cursor.close()
        except:
            pass

    @property
    def cursor(self):
        try:
            return self._cursor
        except:
            self._cursor = self.tx.cursor()
        return self._cursor

    def __call__(self, where=None):
        sql, val = self.sql.select(table=self.name, where=where)
        for data in self.tx.execute(sql, val):
            yield self.row(data)

    def __iter__(self):
        sql, val = self.sql.select(table=self.name, orderby="sys_id")
        for data in self.tx.execute(sql, val):
            yield self.row(data)

    @property
    def sys_columns(self):
        sql, vals = self.sql.columns(self.name)
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        return [x[0] for x in result.as_tuple()]

    @property
    def columns(self):
        columns = []
        for column in self.sys_columns:
            if "sys_" not in column:
                columns.append(column)
        return columns

    @return_default(None, (exceptions.DbObjectExistsError,))
    def create_index(self, columns, unique=False, direction=None, where=None, **kwds):
        sql, vals = self.sql.create_index(
            self.name, columns, unique, direction, where, tbl=self, **kwds
        )
        self.tx.execute(sql, vals, cursor=self.cursor)

    @return_default(None)
    def drop_index(self, columns, **kwds):
        sql, vals = self.sql.drop_index(self.name, columns, **kwds)
        self.tx.execute(sql, vals, cursor=self.cursor)

    @return_default(None)
    def drop_column(self, column):
        sql, vals = self.sql.drop_column(self.name, column)
        self.tx.execute(sql, vals, cursor=self.cursor)

    def create(self, columns={}, drop=False):
        sql, vals = self.sql.create_table(self.name, columns, drop)
        self.tx.execute(sql, vals, cursor=self.cursor)

    def drop(self):
        sql, vals = self.sql.drop_table(self.name)
        self.tx.execute(sql, vals, cursor=self.cursor)

    def exists(self):
        sql, vals = self.sql.tables()
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        if "." in self.name:
            return bool(self.name in ["%s.%s" % x for x in result.as_tuple()])
        else:
            return bool(self.name in ["%s" % x[1] for x in result.as_tuple()])

    def column(self, name):
        return Column(self, name)

    def row(self, key=None, lock=None):
        if key == None:
            return self.new(lock=lock)
        return Row(self, key)

    def dict(self, key):
        row = self.find(key)
        return row.to_dict() if row else {}

    def rows(self, where=None, orderby=None, qty=None, lock=None, skip_locked=None):
        for key in self.ids(
            where=where, orderby=orderby, qty=qty, lock=lock, skip_locked=skip_locked
        ):
            yield Row(self, key, lock=lock)

    def ids(
        self,
        where=None,
        orderby=None,
        groupby=None,
        having=None,
        start=None,
        qty=None,
        lock=None,
        skip_locked=None,
    ):
        for key in self.select(
            "sys_id",
            where=where,
            orderby=orderby,
            groupby=groupby,
            having=having,
            start=start,
            qty=qty,
            lock=lock,
            skip_locked=skip_locked,
        ):
            yield key["sys_id"]

    def set_id(self, start):
        sql, vals = self.sql.set_id(self.name, start)
        result = self.tx.execute(sql, vals, cursor=self.cursor)

    def new(self, data={"sys_modified": "@@CURRENT_TIMESTAMP"}, lock=None):
        if len(data) == 1 and "sys_id" in data:
            return self.row(data, lock=lock).touch()
        val = self.insert(data)
        sql, vals = self.sql.last_id(self.name)
        sys_id = self.tx.execute(sql, vals).scalar()
        return self.row(sys_id, lock=lock)

    def get(self, where, lock=None, use_where=False):
        if where is None:
            raise Exception("None is not allowed as a primary key")
        if isinstance(where, int):
            where = {"sys_id": where}
        result = self.select("sys_id", where=where, lock=lock).all()
        if len(result) > 1:
            sql = self.selectSQL("sys_id", where=where, lock=lock)
            raise exceptions.DuplicateRowsFoundError(
                "More than one entry found. {}".format(sql)
            )
        elif len(result) < 1:
            where = where.copy()
            keys = list(where.keys())
            for key in keys:
                chars = set("<>!=%")
                if any((c in chars) for c in key):
                    where.pop(key)
            return self.new(where, lock=lock)
        if use_where:
            return Row(self, where, lock=lock)
        else:
            return Row(self, result[0]["sys_id"], lock=lock)

    @return_default(None)
    def find(self, where, lock=None, use_where=False):
        if where is None:
            raise Exception("None is not allowed as a primary key")
        if isinstance(where, int):
            where = {"sys_id": where}
        result = self.select("sys_id", where=where, lock=lock).all()
        if len(result) > 1:
            sql = self.selectSQL("sys_id", where=where, lock=lock)
            raise exceptions.DuplicateRowsFoundError(
                "More than one entry found. {}".format(sql)
            )
        elif len(result) < 1:
            return None
        if use_where:
            return Row(self, where, lock=lock)
        else:
            return Row(self, result[0]["sys_id"], lock=lock)

    @return_default(None)
    def first(
        self,
        where,
        orderby=None,
        create_new=False,
        lock=None,
        skip_locked=None,
        use_where=False,
    ):
        if where is None:
            raise Exception("None is not allowed as a where clause")
        if isinstance(where, int):
            where = {"sys_id": where}
        result = self.select(
            "sys_id", where=where, orderby=orderby, skip_locked=skip_locked
        ).all()
        if len(result) < 1:
            if create_new:
                where = where.copy()
                keys = list(where.keys())
                for key in keys:
                    chars = set("<>!=%")
                    if any((c in chars) for c in key):
                        where.pop(key)
                return self.new(where, lock=lock)
            return None
        if use_where:
            return Row(self, where, lock=lock)
        else:
            return Row(self, result[0]["sys_id"], lock=lock)

    @return_default(None)
    def one(self, where=None, orderby=None, lock=None, use_where=False):
        if isinstance(where, int):
            where = {"sys_id": where}
        result = self.select("sys_id", where=where, orderby=orderby).all()
        if len(result) < 1:
            return None
        if use_where:
            return Row(self, where, lock=lock)
        else:
            return Row(self, result[0]["sys_id"], lock=lock)

    @property
    def primary_keys(self):
        sql, vals = self.sql.primary_keys(self.name)
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        return [x[0] for x in result.as_tuple()]

    @property
    def foreign_keys(self):
        sql, vals = self.sql.primary_keys(self.name)
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        return [x[0] for x in result.as_tuple()]

    def foreign_key_info(self, column):
        sql, vals = self.sql.foreign_key_info(table=self.name, column=column)
        return self.tx.execute(sql, vals, cursor=self.cursor).one()

    @return_default()
    def create_foreign_key(self, columns, key_to_table, key_to_columns="sys_id"):
        sql, vals = self.sql.create_foreign_key(
            self.name, columns, key_to_table, key_to_columns
        )
        return self.tx.execute(sql, vals, cursor=self.cursor)

    def drop_foreign_key(self, columns, key_to_table, key_to_columns="sys_id"):
        sql, vals = self.sql.create_foreign_key(
            self.name, columns, key_to_table, key_to_columns
        )
        return self.tx.execute(sql, vals, cursor=self.cursor)

    def rename(self, name):
        sql, vals = self.sql.rename_table(self.name, name)
        self.tx.execute(sql, vals, cursor=self.cursor)
        self.name = name

    def lower_keys(self, arg):
        new = {}
        if isinstance(arg, dict):
            for key in list(arg.keys()):
                new[key.lower()] = arg[key]
        return new

    @create_missing
    def alter(self, columns):
        diff = []
        if isinstance(columns, dict):
            columns = self.lower_keys(columns)
            # Need to maintain order of keys
            for k in list(columns.keys()):
                diff.append(k) if k not in self.sys_columns else None
        else:
            raise Exception(
                "I don't know how to handle columns data type in this context"
            )
        if diff:
            new = dict([(key, columns[key]) for key in diff])
            sql, vals = self.sql.alter_add(self.name, new)
            self.tx.execute(sql, vals, cursor=self.cursor)

    @create_missing
    def alter_type(self, column, type_or_value, nullable=True):
        sql, vals = self.sql.alter_column_by_type(
            self.name, column, type_or_value, nullable
        )
        self.tx.execute(sql, vals, cursor=self.cursor)

    @create_missing
    def update(self, data, pk, left_join=None, inner_join=None, outer_join=None):
        sql, vals = self.sql.update(
            self.name, data, pk, left_join, inner_join, outer_join
        )
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        return result.cursor.rowcount

    @reset_id_on_dup_key
    @create_missing
    def insert(self, data):
        sql, vals = self.sql.insert(self.name, data)
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        return result.cursor.rowcount

    @reset_id_on_dup_key
    @create_missing
    def merge(self, data, pk):
        sql, vals = self.sql.merge(
            self.name, data, pk, on_conflict_do_nothing=False, on_conflict_update=True
        )
        result = self.tx.execute(sql, vals, cursor=self.cursor)
        return result.cursor.rowcount

    upsert = merge
    indate = merge

    def mergeSQL(self, data, pk):
        return self.sql.merge(
            self.name, data, pk, on_conflict_do_nothing=False, on_conflict_update=True
        )

    def insertSQL(self, data):
        return self.sql.insert(self.name, data)

    def updateSQL(self, data, pk, left_join=None, inner_join=None, outer_join=None):
        return self.sql.update(self.name, data, pk, left_join, inner_join, outer_join)

    @return_default(0)
    def count(self, where=None):
        sql, vals = self.sql.select(columns="count(*)", table=self.name, where=where)
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()

    @return_default(0)
    def sum(self, column, where=None):
        sql, vals = self.sql.select(
            columns="coalesce(sum(coalesce({},0)),0)".format(column),
            table=self.name,
            where=where,
        )
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()

    @return_default(0)
    def __len__(self):
        sql, vals = self.sql.select(columns="count(*)", table=self.name)
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()

    @return_default(None)
    def oldest(self, where={}, field="sys_modified", columns="sys_id", lock=None):
        sql, vals = self.sql.select(
            columns=columns,
            table=self.name,
            where=where,
            orderby=field + " asc",
            qty=1,
            lock=lock,
        )
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()

    @return_default(None)
    def newest(self, where={}, field="sys_modified", columns="sys_id", lock=None):
        sql, vals = self.sql.select(
            columns=columns,
            table=self.name,
            where=where,
            orderby=field + " desc",
            qty=1,
            lock=lock,
        )
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()

    @return_default(Result())
    def select(
        self,
        columns=None,
        where=None,
        orderby=None,
        groupby=None,
        having=None,
        start=None,
        qty=None,
        lock=None,
        skip_locked=None,
    ):
        sql, vals = self.sql.select(
            columns=columns,
            table=self.name,
            where=where,
            orderby=orderby,
            groupby=groupby,
            having=having,
            start=start,
            qty=qty,
            tbl=self,
            lock=lock,
            skip_locked=skip_locked,
        )
        return self.tx.execute(sql, vals)

    def list(self, *args, **kwds):
        return self.select(*args, **kwds).all()

    def selectSQL(
        self,
        columns=None,
        where=None,
        orderby=None,
        groupby=None,
        having=None,
        start=None,
        qty=None,
        lock=None,
        skip_locked=None,
    ):
        return self.sql.select(
            columns=columns,
            table=self.name,
            where=where,
            orderby=orderby,
            groupby=groupby,
            having=having,
            start=start,
            qty=qty,
            tbl=self,
            lock=lock,
            skip_locked=skip_locked,
        )

    def query(
        self,
        columns=None,
        where=None,
        orderby=None,
        groupby=None,
        having=None,
        start=None,
        qty=None,
        lock=None,
        skip_locked=None,
    ):
        sql, vals = self.sql.select(
            columns=columns,
            table=self.name,
            where=where,
            orderby=orderby,
            groupby=groupby,
            having=having,
            start=start,
            qty=qty,
            tbl=self,
            lock=lock,
            skip_locked=skip_locked,
        )
        if vals:
            raise Exception(
                "a query generator does not support dictionary type as where clause"
            )
        return Query(sql)

    @return_default(Result())
    def server_select(
        self,
        columns=None,
        where=None,
        orderby=None,
        groupby=None,
        having=None,
        start=None,
        qty=None,
        lock=None,
        skip_locked=None,
    ):
        sql, vals = self.sql.select(
            columns=columns,
            table=self.name,
            where=where,
            orderby=orderby,
            groupby=groupby,
            having=having,
            start=start,
            qty=qty,
            tbl=self,
            lock=lock,
            skip_locked=skip_locked,
        )
        return self.tx.server_execute(sql, vals)

    @return_default(Result())
    def batch(self, size=100, *args, **kwds):
        current = 0
        while True:
            kwds["start"] = current
            kwds["qty"] = size
            results = self.select(*args, **kwds).all()
            if results:
                yield results
                current += len(results)
            else:
                raise StopIteration

    def get_value(self, key, pk):
        return self.select(columns=key, where=pk).scalar()

    @return_default({})
    def get_row(self, where, lock=None):
        if not where:
            raise Exception("Unique key for the row to be retrieved is required.")
        sql, vals = self.sql.select(
            columns="*", table=self.name, where=where, lock=lock
        )
        return self.tx.execute(sql, vals, cursor=self.cursor).one()

    def delete(self, where):
        if not where:
            raise Exception(
                "You just tried to delete an entire table. Use truncate instead."
            )
        sql, vals = self.sql.delete(table=self.name, where=where)
        result = self.tx.execute(sql, vals)
        return result.cursor.rowcount

    def truncate(self):
        sql, vals = self.sql.truncate(table=self.name)
        self.tx.execute(sql, vals)

    def duplicate_rows(self, columns=["sys_id"], where={}, group=False):
        sql, vals = self.sql.duplicate_rows(self.name, columns, where)
        for result in self.tx.execute(sql, vals):
            result.update(where)
            if group:
                yield self.tx.table(self.name).select(where=result).all()
            else:
                for row in self.tx.table(self.name).select(where=result):
                    yield row

    def has_duplicates(self, columns=["sys_id"]):
        sql, vals = self.sql.duplicate_rows(self.name, columns)
        return bool([x for x in self.tx.execute(sql, vals)])

    def create_view(self, name, query, temp=False, silent=True):
        sql, vals = self.sql.create_view(
            name=name, query=query, temp=temp, silent=silent
        )
        return self.tx.execute(sql, vals)

    def drop_view(self, name, silent=True):
        sql, vals = self.sql.drop_view(name=name, silent=silent)
        return self.tx.execute(sql, vals)

    def alter_trigger(self, name="USER", state="ENABLE"):
        sql, vals = self.sql.alter_trigger(table=self.name, state=state, name=name)
        return self.tx.execute(sql, vals)

    def rename_column(self, orig, new):
        sql, vals = self.sql.rename_column(table=self.name, orig=orig, new=new)
        return self.tx.execute(sql, vals)

    def set_sequence(self, next_value=1000):
        sql, vals = self.sql.set_sequence(table=self.name, next_value=next_value)
        return self.tx.execute(sql, vals).scalar()

    def get_sequence(self):
        sql, vals = self.sql.current_id(table=self.name)
        return self.tx.execute(sql, vals).scalar()

    def missing(self, list, column="sys_id", where=None):
        sql, vals = self.sql.missing(
            table=self.name, list=list, column=column, where=where
        )
        return self.tx.execute(sql, vals).as_simple_list().all()

    def lock(self, mode="ACCESS EXCLUSIVE", wait_for_lock=None):
        sql = f"""LOCK TABLE {self.name} IN {mode} MODE"""
        if not wait_for_lock:
            sql += " NOWAIT"
        vals = None
        return self.tx.execute(sql, vals)

    @return_default(0)
    def max(self, column, where=None):
        sql, vals = self.sql.select(
            columns="max({})".format(column), table=self.name, where=where
        )
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()

    @return_default(0)
    def min(self, column, where=None):
        sql, vals = self.sql.select(
            columns="min({})".format(column), table=self.name, where=where
        )
        return self.tx.execute(sql, vals, cursor=self.cursor).scalar()
