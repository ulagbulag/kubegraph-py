'''
# KubeGraph

This is the official Python client library for \
[KubeGraph](https://github.com/ulagbulag/OpenARK/tree/master/templates/kubegraph), \
a service that facilitates the collection and distribution of \
real-time `network graph` information in a cloud-native environment. \
A `network graph` refers to a data structure \
that can be described in terms of nodes and edges. \
This repository enables access to KubeGraph services using Python, \
allowing users to receive network graph information \
and consume it within various data processing and machine learning frameworks, \
including Apache Arrow, Polars, and PyTorch. \
It offers robust and flexible compatibility options.

KubeGraph extracts and stores data in the form of nodes or edges \
from multiple data sources such as Kubernetes, \
[OpenARK](https://github.com/ulagbulag/OpenARK), \
and Prometheus, \
enabling users to tailor data retrieval and storage to their needs.

'''

import os
from typing import Any, List, Optional

import aiohttp
import polars as pl


__all__ = [
    'KubeGraphClient',
]


class KubeGraphClient:
    '''
    This is a Python client class for receiving and processing network graph information \
    from the `KubeGraph` service.
    '''

    def __init__(
        self,
        url: Optional[str] = None,
    ) -> None:
        self._url = os.environ.get('KUBEGRAPH_URL', url)
        if self._url is None:
            raise ValueError('Environment Variable not set: "KUBEGRAPH_URL"')

        self._session = aiohttp.ClientSession()

    async def get_entries(self) -> List[Any]:
        '''
        Receives network graph information from the `KubeGraph` service \
        and converts it into a `JSON` list format.
        '''
        async with self._session as session:
            async with session.get(self._url) as response:
                body = await response.json(encoding='utf-8')

        if not isinstance(body, dict):
            raise ValueError('Malformed response on getting entries')

        if body.get('result', 'err') != 'ok' or body.get('spec', None) is None:
            raise ValueError(body.get(
                'spec',
                'Failed to execute getting entries',
            ))

        return body['spec']

    async def to_polars(self) -> pl.DataFrame:
        '''
        Receives network graph information from the `KubeGraph` service
        and converts it into a Polars `DataFrame` format.
        '''
        return to_polars(await self.get_entries())


def to_polars(entries: List[Any]) -> pl.DataFrame:
    '''
    Converts the network graph information in `JSON` list format
    into a Polars `DataFrame` format.
    '''
    return pl.DataFrame(entries)


def to_polars_edges(df: pl.DataFrame) -> pl.DataFrame:
    '''
    Extracts edges from the network graph information in Polars `DataFrame` format
    and creates and stores a new `DataFrame`.
    '''
    return df.filter(df['type'] == 'edge')[[
        'link_kind', 'link_name', 'link_namespace',
        'src_kind', 'src_name', 'src_namespace',
        'sink_kind', 'sink_name', 'sink_namespace',
        'le', 'value',
    ]]


def to_polars_nodes(df: pl.DataFrame) -> pl.DataFrame:
    '''
    Extracts nodes from the network graph information in Polars `DataFrame` format
    and creates and stores a new `DataFrame`.
    '''
    return df.filter(df['type'] == 'node')[[
        'kind', 'name', 'namespace',
        'le', 'value',
    ]]
