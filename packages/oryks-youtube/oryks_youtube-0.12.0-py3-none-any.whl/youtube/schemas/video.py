from datetime import datetime
from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel, Field

from .youtube_request import Filter, OptionalParameters, Part


class VideoPart(Part):
    part: list[str] = Field(
        default=[
            'contentDetails',
            'id',
            'liveStreamingDetails',
            'localizations',
            'player',
            'recordingDetails',
            'snippet',
            'statistics',
            'status',
            'topicDetails',
        ]
    )


class Rating(Enum):
    like = auto()
    dislike = auto()


class VideoFilter(Filter):
    chart: Optional[str] = ''
    id: Optional[list[str]] = Field(default_factory=list)
    myRating: Optional[str] = ''


class VideoOptionalParameters(OptionalParameters):
    h1: Optional[str] = ''
    maxHeight: Optional[int] = None
    maxResults: Optional[int] = None
    maxWidth: Optional[int] = None
    onBehalfOfContentOwner: Optional[str] = ''
    pageToken: Optional[str] = ''
    regionCode: Optional[str] = ''
    videoCategoryId: Optional[str] = ''


class UploadVideoSnippet(BaseModel):
    title: str
    description: str
    categoryId: str
    defaultLanguage: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class UploadVideoLocalizations(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class UploadVideoStatus(BaseModel):
    embeddable: Optional[bool] = None
    license: Optional[str] = None
    privacyStatus: Optional[str] = None
    publicStatsViewable: Optional[bool] = None
    publishAt: Optional[datetime] = None
    selfDeclaredMadeForKids: Optional[str] = None


class UploadVideoRecordingDetails(BaseModel):
    recordingDate: Optional[datetime] = None


class UploadVideo(BaseModel):
    file: str
    snippet: UploadVideoSnippet
    localizations: Optional[UploadVideoLocalizations] = None
    status: Optional[UploadVideoStatus] = None
    recordingDetails: Optional[UploadVideoRecordingDetails] = None
