from enum import Enum, auto

from pydantic import BaseModel, Field

from .resource import Resource


class ChannelSectionSnippet(BaseModel):
    type: str
    channel_id: str
    title: str
    position: int


class ChannelSectionContentDetails(BaseModel):
    playlists: list[str] = Field(default_factory=list)
    channels: list[str] = Field(default_factory=list)


class ChannelSection(Resource):
    snippet: ChannelSectionSnippet
    content_details: ChannelSectionContentDetails


class ChannelSectionType(Enum):
    allPlaylists = 'allPlaylists'
    completedEvents = 'completedEvents'
    liveEvents = 'liveEvents'
    multipleChannels = 'multipleChannels'
    multiplePlaylists = 'multiplePlaylists'
    popularUploads = 'popularUploads'
    recentUploads = 'recentUploads'
    singlePlaylist = 'singlePlaylist'
    subscriptions = 'subscriptions'
    upcomingEvents = 'upcomingEvents'
