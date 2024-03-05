from .interfaces import Pool
from .operation import Operation


class Transaction(object):
    def __init__(self, pool: Pool):
        self._pool = pool
        self._ops: list[Operation] = []

    def add(self, *ops: Operation):
        for op in ops: self._ops.append(op)
        return self

    async def commit(self):
        async with self._pool.acquire() as connection:
            # for some reason transaction is None
            async with connection.transaction() as transaction:
                print('type of transaction', type(transaction))
                for op in self._ops:
                    op.results = await connection.execute(op.sql, *op.parameters)
