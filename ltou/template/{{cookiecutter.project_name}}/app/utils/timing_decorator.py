import asyncio
import time
from functools import wraps
from typing import Callable


def timeit(func) -> Callable:

    async def inner_process(fun: Callable, *args, **params):
        if asyncio.iscoroutinefunction(func):
            print('this function is a coroutine: {}'.format(func.__name__))
            return await fun(*args, **params)
        else:
            print('this is not a coroutine')
            return func(*args, **params)

    @wraps(func)
    async def helper(*args, **params) -> Callable:
        print('{}.time'.format(func.__name__))
        start = time.time()
        result = await inner_process(func, *args, **params)

        print('>>>', time.time() - start)
        return result

    return helper


if __name__ == '__main__':
    @timeit
    async def foo():
        return await asyncio.sleep(2, result="async function done")
    asyncio.run(foo())