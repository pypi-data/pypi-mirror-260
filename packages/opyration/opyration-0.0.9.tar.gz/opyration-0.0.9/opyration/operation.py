from .interfaces import Pool
from .results import Results
from .symbols import SYMBOLS


class Safe(object):
    def __init__(self, sql):
        self.__sql = sql

    @property
    def sql(self):
        return self.__sql


class Operation(object):
    def __init__(self, table: str, pool: Pool = None, schema=''):
        self.__table = table
        self.__schema = f'{schema}.' if schema else '' 
        self.__pool = pool
        self.__cols = None
        self.__vals = None
        self.__sql = None
        self.__asking = False
        self.__affected = 0
        self.__results = None
        self.__page = 0

    def _parameterize(self, **pairs):
        self.__vals = []
        keys, vals = [], []
        for k, v in pairs.items():
            keys.append(k)
            if isinstance(v, Safe): vals.append(v.sql)
            else:
                vals.append(f'${len(vals) + 1}')
                self.__vals.append(v)
        return keys, vals

    @staticmethod
    def _placeholders(keys):
        return ', '.join([f'${i}' for i in range(1, len(keys) + 1)])

    @property
    def affected(self):
        return self.__affected

    @affected.setter
    def affected(self):
        raise ValueError('Read only field can not be set')

    @property
    def all(self):
        return self.__results

    def asc(self, *columns):
        self.__sql = f'{self.__sql} ORDER BY {", ".join(columns)} ASC'
        return self

    @property
    def columns(self):
        return self.__cols

    @columns.setter
    def columns(self, *cols: list):
        self.__cols = ', '.join(cols)

    def desc(self, *columns):
        self.__sql = f'{self.__sql} ORDER BY {", ".join(columns)} DESC'
        return self

    @property
    def parameters(self):
        return self.__vals

    @property
    def json(self):
        return [dict(datum) for datum in self.__results]
    
    @property
    def fetching(self):
        return self.__asking

    async def first(self):
        async with self.__pool.acquire() as connection:
            return await connection.fetchrow(self.__sql, *self.__vals)

    def delete(self):
        self.__vals = []
        self.__sql = f'''DELETE FROM {self.__schema}{self.__table}'''
        return self

    def parens_where(self, conditions: dict):
        start = len(self.__vals)
        prepending_symbol, sql = '', ''

        for index, pair in enumerate(conditions.items()):
            sym_field, value = pair
            sym, field_op = sym_field[0], sym_field[1:]
            if sym not in ['&', '|']: raise ValueError('Invalid conjuction symbol')

            if isinstance(value, Operation): value = f'({value.sql})'
            self.__vals.append(value)

            placeholder = f'${start + index + 1}'
            conjunctor = {'&': 'AND', '|': 'OR'}[sym]
            if index == 0:
                prepending_symbol = conjunctor
                conjunctor = ''

            try: field, op = field_op.split('__')
            except: field, op = field_op, 'eq'
            op = SYMBOLS[op]

            sql = f"{sql} {conjunctor} {field}{op}{placeholder}"
        self.__sql = f'{self.__sql} {prepending_symbol} ({sql})'
        return self

    def insert(self, **pairs):
        if self.__vals or self.__sql: raise ValueError('Operations can not be reused...')
        keys, placeholders = self._parameterize(**pairs)  # parameterize saves vals and returns keys and placeholders
        self.__sql = f'''INSERT INTO {self.__schema}{self.__table} ({', '.join(keys)}) VALUES ({', '.join(placeholders)})'''
        return self
    
    def __join(self, join_type, **conditions):
        for key, value in conditions.items():
            table, column = key.split('__')
            self.__sql = f'{self.__sql} {join_type} {self.__schema}{table} ON {table}.{column}={value}'
        return self

    def join(self, **conditions):
        return self.__join('JOIN', **conditions)
    
    def left_join(self, **conditions):
        return self.__join('LEFT JOIN', **conditions)
    
    def right_join(self, **conditions):
        return self.__join('RIGHT JOIN', **conditions)

    def limit(self, limit: int):
        self.__sql = f'{self.__sql} LIMIT {limit}'

    def or_where(self, **pairs):
        start = len(self.__vals)
        for field_op, value in pairs.items():
            placeholder = f'${start + 1}'
            try: field, op = field_op.split('__')
            except: field, op = field_op, 'eq'
            sym = SYMBOLS[op]
            suffix = f"OR {field}{sym}{placeholder}"
            if isinstance(value, Operation): value = f'({value.sql})'
            self.__vals.append(value)
            self.__sql = f'{self.__sql} {suffix}'
        return self

    def page(self, page: int):
        self.__pagination.limit = page

    @property
    def raw(self):
        # use self.sql and self.parameters to replace $1, $2, etc with values
        sql = self.sql
        for index, value in enumerate(self.parameters):
            sql = sql.replace(f'${index + 1}', str(value))
        return sql

    def raw(self, sql: str):
        self.__sql = sql
        return self

    def refresh(self):
        self.__page = 0
        self.__schema = ''
        self.__cols = None
        self.__vals = None
        self.__sql = None
        self.__asking = False
        self.__affected = 0
        self.__results = None
        return self

    @property
    def results(self):
        return Results(self.__results)

    @results.setter
    def results(self, results):
        if self.__results: raise ValueError('Results is not writable once set')
        self.__results = results

    def returning(self, *columns):
        self.__asking = True
        columns = ', '.join(columns) if columns else '*'
        self.__sql = f'{self.__sql} RETURNING {columns}'
        return self

    async def run(self):
        async with self.__pool.acquire() as connection:
            async with connection.transaction() as transaction:
                if self.__asking:
                    self.__results = await connection.fetch(self.__sql, *self.__vals)
                else: self.__affected = await connection.execute(self.__sql, *self.__vals)
        return self

    def safe(self, sql) -> Safe:
        return Safe(sql)

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema: str):
        self.__schema = f'{schema}.'

    async def execute(self, sql: str, *vals):
        return await self.__command(sql, *vals)

    async def fetch(self, sql: str, *vals):
        self.__asking = True
        return await self.__command(sql, *vals)

    async def __command(self, sql: str, *vals):
        async with self.__pool.acquire() as connection:
            async with connection.transaction() as transaction:
                if self.__asking:
                    self.__results = await connection.fetch(sql, *vals)
                else: self.__affected = await connection.execute(sql, *vals)
        return self

    def select(self, *columns):
        self.__vals = []
        self.__asking = True
        columns = ', '.join(columns) if columns else '*'
        self.__sql = f'''SELECT {columns} FROM {self.__schema}{self.__table}'''
        return self

    @property
    def sql(self):
        return self.__sql

    def update(self, **pairs):
        self.__vals = []
        self.__sql = f'UPDATE {self.__schema}{self.__table} SET'
        start = len(self.__vals)
        equations = []
        for index, pair in enumerate(pairs.items()):
            field, value = pair
            if isinstance(value, Safe):
                placeholder = value.sql
            else:
                placeholder = f'${index + start + 1}'
                self.__vals.append(value)

            equations.append(f'{field}={placeholder}')
        self.__sql = f'{self.__sql} {", ".join(equations)}'
        return self

    def where(self, **conditions):
        # get length already in vars and add to index
        start = len(self.__vals)
        for index, pair in enumerate(conditions.items()):
            placeholder = f'${index + start + 1}'
            field_op, value = pair
            try:
                args = field_op.split('__')
                if len(args) == 2: field, op = args
                else:
                    t, field, op = args
                    field = f'{t}.{field}'
            except: field, op = field_op, 'eq'
            sym = SYMBOLS[op]
            clause = 'WHERE' if index == 0 else 'AND'
            suffix = f"{clause} {field}{sym}{placeholder}"
            if isinstance(value, Operation): value = f'({value.sql})'
            self.__vals.append(value)
            self.__sql = f'{self.__sql} {suffix}'
        return self
