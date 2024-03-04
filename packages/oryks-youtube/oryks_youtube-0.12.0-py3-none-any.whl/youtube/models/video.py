from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .resource import Resource
from .thumbnail import Thumbnail


class RegionRestriction(BaseModel):
    allowed: list[str] = Field(default_factory=list)
    blocked: list[str] = Field(default_factory=list)


class ContentRating(BaseModel):
    pass


class Status(BaseModel):
    upload_status: str
    failure_reason: str
    rejection_reason: str
    privacy_status: str
    publish_at: datetime
    license: str
    embedabble: bool
    public_stats_viewable: bool
    made_for_kids: bool
    self_declared_made_for_kids: bool


class Statistics(BaseModel):
    views_count: int
    likes_count: int
    comments_count: int


class Localized(BaseModel):
    title: str
    description: str


class Snippet(BaseModel):
    title: str
    channel_id: str
    channel_title: str
    description: str
    thumbnails: Thumbnail
    tags: list[str] = Field(default_factory=list)
    published_at: datetime
    category_id: str
    live_broadcast_content: str
    default_language: str = None
    localized: Localized


class ContentRatings(BaseModel):
    pass


class ContentDetails(BaseModel):
    duration: str
    dimension: str
    definition: str
    caption: str
    licensed_content: bool
    # content_ratings: ContentRatings
    projection: str
    has_custom_thumbnail: Optional[bool] = None
    region_restriction: Optional[RegionRestriction] = RegionRestriction()


class Video(Resource):
    id: str
    snippet: Snippet
    content_details: ContentDetails
    # status: Status
    statistics: Statistics
