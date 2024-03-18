import asyncio
from pprint import pprint as print

from kubegraph import KubeGraphClient



async def main():
    client = KubeGraphClient()
    print(await client.get_entries())


if __name__ == '__main__':
    asyncio.run(main())
