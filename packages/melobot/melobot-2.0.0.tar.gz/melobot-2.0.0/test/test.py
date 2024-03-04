import asyncio as aio
import sys
import time
from asyncio import iscoroutine, iscoroutinefunction
from functools import wraps

sys.path.append("E:\\projects\\Python\\git-proj\\melobot_renew")
from melobot.types.exceptions import *
from melobot.types.typing import *
from melobot.utils.base import cooldown, lock, semaphore


async def aprint(s: str) -> None:
    print(s)


@cooldown(lambda: aprint("冲突..."), lambda t: aprint(f"冷却时间还剩 {t}s"))
async def work(x: int) -> None:
    await aio.sleep(1)
    print(x)


@semaphore(lambda: aprint("冲突..."), value=3)
async def work2(x: int) -> None:
    await aio.sleep(1)
    print(x)


async def main():
    await work(1)
    await aio.sleep(1)
    await work(2)
    await aio.sleep(1)
    await work(3)
    await aio.sleep(1)
    await work(4)
    await aio.sleep(1)
    await work(5)
    await aio.sleep(1)
    await work(6)


aio.run(main())
