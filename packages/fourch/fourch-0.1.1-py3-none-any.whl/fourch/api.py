from enum import Enum
from http import HTTPMethod
from typing import Optional
from const import Board, Category, Special, Other, International
from models import Model, Thread
from session import AsyncRequestSession


class FourCH:
    
    API_HOST = 'https://a.4cdn.org'
    HOST_ATTACHMENT = 'https://i.4cdn.org'
    
    def __init__(self, board: Enum = Optional[Board | Category | Special | Other | International]) -> None:
        self.board = board.value
        self.session = AsyncRequestSession()
    
    async def get_post(self, page: int = 1) -> Model:
        async with AsyncRequestSession() as session:
            url = f'{self.API_HOST}/{self.board}/{page}.json'
            response = await session._validate_response(HTTPMethod.GET.value, url=url)
        
        return Model(**response)
    
    async def get_all_attachnemts(self, no: int):
        async with AsyncRequestSession() as session:
            url = f'{self.API_HOST}/{self.board}/thread/{no}.json'
            response = await session._validate_response(HTTPMethod.GET.value, url=url)
            threads: Thread = Thread(**response)
            attachment = []
            sub = None
            for post in threads.posts:
                if sub is None and post.sub: sub = post.sub
                if post.filename and post.ext and post.filename != 'Untitled':
                    attachment.append(f'{self.HOST_ATTACHMENT}/{self.board}/{post.tim}{post.ext}')
            return {sub: attachment}
    
    async def get_attachments_in_thread(self, page: int = 1) -> list[str]:
        async with AsyncRequestSession() as session:
            url = f'{self.API_HOST}/{self.board}/{page}.json'
            response = await session._validate_response(HTTPMethod.GET.value, url=url)
        
        threads: Model = Model(**response)
        attachment = []

        for thread in threads.threads:
            for post in thread.posts:
                if post.filename and post.ext and post.filename != 'Untitled':
                    attachment.append({post.sub or 'Anonimus': f'{self.HOST_ATTACHMENT}/{self.board}/{post.tim}{post.ext}'})
        return attachment
                    
                
        
    
    