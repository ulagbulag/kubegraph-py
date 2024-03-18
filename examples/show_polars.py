#!/usr/bin/env python3

'''
This is an example of outputting the original network graph JSON
obtained from the server to stdout.
'''

import asyncio
from pprint import pprint

from kubegraph import KubeGraphClient, to_polars_edges, to_polars_nodes


async def main():
    '''This is the main function of the example.'''

    client = KubeGraphClient()
    df = await client.to_polars()

    print('* Nodes')
    nodes = to_polars_nodes(df)
    pprint(nodes)
    print()

    print('* Edges')
    edges = to_polars_edges(df)
    pprint(edges)
    print()


if __name__ == '__main__':
    asyncio.run(main())
