from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .content_details import BaseContentDetails
from .resource import Resource
from .snippet import BaseSnippet
from .status import BaseStatus


class ChannelSnippet(BaseSnippet):
    custom_url: str
    country: str


class RelatedPlaylists(BaseModel):
    likes: str = Field(
        description="The ID of the playlist that contains the channel's liked videos."
    )
    uploads: str


class ChannelContentDetails(BaseContentDetails):
    related_playlists: RelatedPlaylists


class ChannelStatistics(BaseModel):
    views_count: int
    subscribers_count: int
    hidden_subscribers_count: bool
    videos_count: int


class ChannelStatus(BaseStatus):
    is_linked: bool
    long_uploads_status: str
    made_for_kids: bool


class Channel(Resource):
    content_details: ChannelContentDetails
    statistics: ChannelStatistics
    status: ChannelStatus
