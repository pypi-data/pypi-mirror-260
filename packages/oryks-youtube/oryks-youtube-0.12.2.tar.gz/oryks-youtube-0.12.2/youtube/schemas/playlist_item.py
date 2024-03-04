from typing import Optional

from pydantic import BaseModel, Field

from .youtube_request import Filter, OptionalParameters, Part


class PlaylistItemPart(Part):
    part: list[str] = Field(default=['contentDetails', 'id', 'snippet', 'status'])


class PlaylistItemFilter(Filter):
    playlistId: Optional[str] = ''


class PlaylistItemOptionalParameters(OptionalParameters):
    maxResults: Optional[int] = None
    onBehalfOfContentOwner: Optional[str] = ''
    videoId: Optional[str] = ''
    pageToken: Optional[str] = ''


class VideoResourceId(BaseModel):
    videoId: str
    kind: Optional[str] = 'youtube#video'


class CreatePlaylistItemSnippet(BaseModel):
    playlistId: str
    resourceId: VideoResourceId
    position: Optional[int] = 0


class CreatePlaylistItem(BaseModel):
    snippet: CreatePlaylistItemSnippet
