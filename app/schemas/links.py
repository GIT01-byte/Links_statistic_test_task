import datetime
from typing import List
from pydantic import BaseModel


class LinksCreateRequest(BaseModel):
    links: List[str]

class LinksRequestWthTimestamp(LinksCreateRequest):
    received_at: int

class LinksCreateDTO(BaseModel):
    link: str
    timestamp: int

class LinksDTO(LinksCreateDTO):
    id: int
