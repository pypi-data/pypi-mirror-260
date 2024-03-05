import asyncio
from typing import Optional, Dict, Any
import aiohttp
from exceptions import ErrorFactory

class AsyncRequestSession:
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
        self._loop = asyncio.get_event_loop()

    async def __aenter__(self) -> "AsyncRequestSession":
        await self.get_session()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close_session()

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            connector = aiohttp.TCPConnector(ssl=False)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}
            self._session = aiohttp.ClientSession(connector=connector, headers=headers)
        return self._session

    async def close_session(self) -> None:
        if self._session:
            await self._session.close()

    async def _validate_response(self, method: str, url: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        session = await self.get_session()

        async with session.request(method, url=url, data=data) as response:
            try:
                response_data = await response.json(content_type='application/json')
            except aiohttp.ContentTypeError:
                raise ErrorFactory(response.status, "Response is not in JSON format")
            
            if response_data.get("status") == "error":
                desc = response_data.get("text", response_data.get("error_text"))
                code = response_data.get("error_code", response.status)
                raise ErrorFactory(code, desc)

            return response_data

    async def close(self) -> None:
        await self.close_session()

    def __del__(self) -> None:
        asyncio.ensure_future(self.close(), loop=self._loop)
