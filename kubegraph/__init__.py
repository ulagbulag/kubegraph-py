import aiohttp
import os
from typing import Any, List, Optional

import polars as pl


__all__ = [
    'KubeGraphClient',
]


class KubeGraphClient:
    def __init__(
        self,
        url: Optional[str] = None,
    ) -> None:
        self._url = os.environ.get('KUBEGRAPH_URL', url)
        if self._url is None:
            raise ValueError('Environment Variable not set: "KUBEGRAPH_URL"')
        
        self._session = aiohttp.ClientSession()

    async def get_entries(self) -> List[Any]:
        async with self._session as session:
            async with session.get(self._url) as response:
                body = await response.json(encoding='utf-8')
        
        if not isinstance(body, dict):
            raise ValueError('Malformed response on getting entries')

        if body.get('result', 'err') != 'ok' or body.get('spec', None) is None:
            raise Exception(body.get('spec', 'Failed to execute getting entries'))
        
        return body['spec']

    async def to_polars(self) -> pl.DataFrame:
        return to_polars(await self.get_entries())


def to_polars(entries: List[Any]) -> pl.DataFrame:
    return pl.DataFrame(entries)


def to_polars_edges(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(df['type'] == 'edge')[[
        'link_kind', 'link_name', 'link_namespace',
        'src_kind', 'src_name', 'src_namespace',
        'sink_kind', 'sink_name', 'sink_namespace',
        'le', 'value',
    ]]


def to_polars_nodes(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(df['type'] == 'node')[[
        'kind', 'name', 'namespace',
        'le', 'value',
    ]]
