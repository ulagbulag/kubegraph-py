#!/usr/bin/env python3

'''
This is an example of dividing the network graph
obtained from the server into nodes and edges
and saving each as a `.csv` file in the current working directory.
'''

import asyncio

from kubegraph import KubeGraphClient, to_polars_edges, to_polars_nodes


async def main():
    '''This is the main function of the example.'''

    client = KubeGraphClient()
    df = await client.to_polars()

    nodes_path = 'nodes.csv'
    print(f'* Nodes: {nodes_path!r}')
    with open(nodes_path, 'w', encoding='utf-8') as f:
        to_polars_nodes(df).write_csv(f)

    edges_path = 'edges.csv'
    print(f'* Edges: {edges_path!r}')
    with open(edges_path, 'w', encoding='utf-8') as f:
        to_polars_edges(df).write_csv(f)


if __name__ == '__main__':
    asyncio.run(main())
