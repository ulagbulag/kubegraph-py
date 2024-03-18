import asyncio
from pprint import pprint

from kubegraph import KubeGraphClient



async def main():
    client = KubeGraphClient()
    pprint(await client.get_entries())


if __name__ == '__main__':
    asyncio.run(main())
