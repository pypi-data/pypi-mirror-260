import asyncio
import sys

sys.path.append(r"E:\projects\Python\git-proj\melobot")
from dev.plugins.public_utils import FormData, async_http, get_headers


async def main():
    with open(r"2939fc304d7d88447f460b76aa9d7199.jpeg", "rb") as fp:
        image = fp.read()
    url = "https://api.trace.moe/search?cutBorders"
    data = FormData()
    data.add_field("image", image)
    async with async_http(url, method="post", headers=get_headers(), data=data) as resp:
        res = await resp.json()
        print(res)


asyncio.run(main())
