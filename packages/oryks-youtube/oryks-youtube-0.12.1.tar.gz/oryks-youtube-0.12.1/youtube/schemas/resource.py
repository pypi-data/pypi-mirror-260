from typing import Optional

from pydantic import BaseModel, Field

from .common import PageInfo
from .resource_schema import Resource


class Part(BaseModel):
    pass


class Filter(BaseModel):
    pass


class OptionalParameters(BaseModel):
    pass


class RequestSchema(BaseModel):
    part: Part
    filter: Optional[Filter] = Filter()
    optional_parameters: Optional[OptionalParameters] = OptionalParameters()


class YouTubeResponse(BaseModel):
    kind: str
    etag: str
    pageInfo: PageInfo
    items: list[Resource] = Field(default_factory=list)
    nextPageToken: Optional[str] = ''
    prevPageToken: Optional[str] = ''
