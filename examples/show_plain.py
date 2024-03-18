#!/usr/bin/env python3

'''
This is an example of dividing the network graph
obtained from the server into nodes and edges
and outputting it to stdout.
'''

import asyncio
from pprint import pprint

from kubegraph import KubeGraphClient


async def main():
    '''This is the main function of the example.'''

    client = KubeGraphClient()
    pprint(await client.get_entries())


if __name__ == '__main__':
    asyncio.run(main())
