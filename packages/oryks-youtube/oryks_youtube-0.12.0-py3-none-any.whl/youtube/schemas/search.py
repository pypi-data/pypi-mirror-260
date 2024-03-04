from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .youtube_request import Filter, OptionalParameters, Part


class SearchPart(Part):
    part: list[str] = Field(default=['snippet'])


class SearchFilter(Filter):
    forContentOwner: Optional[str] = ''
    forDeveloper: Optional[str] = ''
    forMine: Optional[str] = ''


class ChannelType(Enum):
    any = 'any'
    show = 'show'


class EventType(Enum):
    completed = 'completed'
    live = 'live'
    upcoming = 'upcoming'


class Order(Enum):
    date = 'date'
    rating = 'rating'
    relevance = 'relevance'
    title = 'title'
    videoCount = 'videoCount'
    viewCount = 'viewCount'


class VideoType(Enum):
    any = 'any'
    episode = 'episode'
    movie = 'movie'


class VideoSyndicated(Enum):
    any = 'any'
    true = 'true'


class VideoPaidProductPlacement(Enum):
    any = 'any'
    true = 'true'


class VideoLicense(Enum):
    any = 'any'
    creativeCommon = 'creativeCommon'
    youtube = 'youtube'


class VideoEmbeddable(Enum):
    videoEmbeddableUnspecified = 'videoEmbeddableUnspecified'
    true = 'true'
    any = 'any'


class VideoDuration(Enum):
    any = 'any'
    long = 'long'
    medium = 'medium'
    short = 'short'


class VideoDimension(Enum):
    any = 'any'
    two_d = '2d'
    three_d = '3d'


class VideoDefinition(Enum):
    any = 'any'
    high = 'high'
    standard = 'standard'


class VideoCaption(Enum):
    any = 'any'
    closedCaption = 'closedCaption'
    none = 'none'


class Type(Enum):
    video = 'video'
    channel = 'channel'
    playlist = 'playlist'


class SafeSearch(Enum):
    moderate = 'moderate'
    none = 'none'
    strict = 'strict'


class SearchOptionalParameters(OptionalParameters):
    channelId: Optional[str] = ''
    channelType: Optional[str] = ChannelType.any.value
    eventType: Optional[str] = ''
    location: Optional[str] = ''
    locationRadius: Optional[str] = ''
    maxResults: Optional[int] = 25
    onBehalfOfContentOwner: Optional[str] = ''
    order: Optional[str] = Order.relevance.value
    pageToken: Optional[str] = ''
    publishedAfter: Optional[str] = ''
    publishedBefore: Optional[str] = ''
    regionCode: Optional[str] = ''

    q: Optional[str] = ''
    relevanceLanguage: Optional[str] = ''
    safeSearch: Optional[str] = SafeSearch.none.value
    topicId: Optional[str] = ''
    type: Optional[list[str]] = Field(
        default=[Type.channel.value, Type.video.value, Type.playlist.value]
    )

    videoCaption: Optional[str] = ''
    videoCategoryId: Optional[str] = ''
    videoDefinition: Optional[str] = ''
    videoDimension: Optional[str] = ''
    videoDuration: Optional[str] = ''

    videoEmbeddable: Optional[str] = ''
    videoLicense: Optional[str] = VideoLicense.any.value
    videoPaidProductPlacement: Optional[str] = ''
    videoSyndicated: Optional[str] = ''
    videoType: Optional[str] = ''
