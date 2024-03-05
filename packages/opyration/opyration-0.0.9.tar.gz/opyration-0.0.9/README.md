# Opyration

SQL and Python should be simple right? Sometimes code is better than extensive explanation - see snippets below:

```py
from opyration import Operation


pool = ...  # in production use an asyncpg|aiomysql Pool()


# example 1
op = Operation('customers', ...).select().where(location='California', age__gt=18)
await op.run()


# example 2
op = Operation('products', ...)
op.select()
op..where(username='; drop customers')
assert op.sql = 'SELECT * FROM products WHERE id = $1'
```

## Installling
Install with [pip](https://pip.pypa.io/en/stable/getting-started/)
```sh
$ pip install opyration
```

## More Examples
<hr/>

```py
from opyration import Operation

op = Operation()
op.update(username='new username').where(id='1ea-455-bc0-88a')

# to run in sync mode use: op.runs()
await op.run()  # async
```

## Contributing

For guidance on how to make contributions to opyration, see the [Contribution Guidelines](contributions.md)


## Links

- Documentation [Go To Docs](https://rayattack.github.io/opyration)
- PyPi [https://pypi.org/project/heaven](https://pypi.org/project/opyration)
- Source Code [Github](https://github.com/rayattack/opyration)
