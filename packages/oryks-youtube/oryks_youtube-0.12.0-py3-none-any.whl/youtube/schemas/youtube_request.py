from typing import Optional

from pydantic import BaseModel, Field


class Part(BaseModel):
    pass


class Filter(BaseModel):
    id: Optional[list[str]] = Field(default_factory=list)


class OptionalParameters(BaseModel):
    pass


class YouTubeRequest(BaseModel):
    part: Part
    filter: Optional[Filter] = Filter()
    optional_parameters: Optional[OptionalParameters] = OptionalParameters()
