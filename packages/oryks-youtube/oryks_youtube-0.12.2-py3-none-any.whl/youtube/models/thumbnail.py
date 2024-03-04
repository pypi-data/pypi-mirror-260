from typing import Optional

from pydantic import BaseModel


class ThumbnailResolution(BaseModel):
    url: str
    width: int
    height: int


class Thumbnail(BaseModel):
    default: Optional[ThumbnailResolution] = None
    medium: Optional[ThumbnailResolution] = None
    high: Optional[ThumbnailResolution] = None
    standard: Optional[ThumbnailResolution] = None
    maxres: Optional[ThumbnailResolution] = None
