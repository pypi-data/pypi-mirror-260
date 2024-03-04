from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.resource import Resource
from .localized import Localized
from .thumbnail import Thumbnail


class Snippet(BaseModel):
    title: str
    channel_id: str
    channel_title: str
    description: str
    thumbnails: Thumbnail
    published_at: datetime
    default_language: str = None
    localized: Localized


class Status(BaseModel):
    privacy_status: str


class ContentDetails(BaseModel):
    item_count: int


class Playlist(Resource):
    id: str
    snippet: Optional[Snippet] = None
    status: Optional[Status] = None
    content_details: Optional[ContentDetails] = None
