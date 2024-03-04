from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.resource import Resource
from .resource_id import ResourceId
from .status import Status
from .thumbnail import Thumbnail


class Snippet(BaseModel):
    title: str
    channel_id: str
    channel_title: str
    description: str
    thumbnails: Thumbnail
    playlist_id: str
    resource_id: ResourceId
    video_owner_channel_title: Optional[str] = None
    video_owner_channel_id: Optional[str] = None
    published_at: Optional[datetime] = None
    position: Optional[int] = 0


class ContentDetails(BaseModel):
    video_id: str
    video_published_at: Optional[datetime] = None
    note: Optional[str] = ''


class PlaylistItem(Resource):
    id: str
    snippet: Snippet
    content_details: Optional[ContentDetails] = None
    status: Optional[Status] = None
