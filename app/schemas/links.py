from typing import List

from pydantic import BaseModel, Field


class LinksCreateRequest(BaseModel):
    links: List[str]

class LinksRequestWthTimestamp(LinksCreateRequest):
    received_at: int

class LinksCreateDTO(BaseModel):
    link: str
    timestamp: int

class LinksDTO(LinksCreateDTO):
    id: int

class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, le=100, description='Кол-вщ элементов на странице')
    offset: int = Field(0, ge=0, description='Смещение дял пагинации')
