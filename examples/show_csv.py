import asyncio

from kubegraph import KubeGraphClient, to_polars_edges, to_polars_nodes



async def main():
    client = KubeGraphClient()
    df = await client.to_polars()

    nodes_path = 'nodes.csv'
    print(f'* Nodes: {nodes_path!r}')
    with open(nodes_path, 'w') as f:
        to_polars_nodes(df).write_csv(f)

    edges_path = 'edges.csv'
    print(f'* Edges: {edges_path!r}')
    with open(edges_path, 'w') as f:
        to_polars_edges(df).write_csv(f)


if __name__ == '__main__':
    asyncio.run(main())
