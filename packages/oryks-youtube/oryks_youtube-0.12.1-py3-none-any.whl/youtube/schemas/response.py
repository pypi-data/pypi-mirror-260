from pydantic import BaseModel, Field

from .resource import Resource


class Response(BaseModel):
    kind: str
    etag: str
    items: list[Resource] = Field(default_factory=list)
