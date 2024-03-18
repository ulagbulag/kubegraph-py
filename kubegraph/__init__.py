import aiohttp
import os
from typing import Any, List, Optional


__all__ = [
    'KubeGraphClient',
]


class KubeGraphClient:
    def __init__(
        self,
        url: Optional[str] = None,
    ) -> None:
        self._url = os.environ.get('KUBESPRAT_PATH', url)
        if self._url is None:
            raise ValueError('Environment Variable not set: "KUBESPRAT_PATH"')
        
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
