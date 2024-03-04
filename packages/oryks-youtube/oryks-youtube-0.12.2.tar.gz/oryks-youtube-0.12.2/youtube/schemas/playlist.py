from typing import Optional

from pydantic import BaseModel, Field

from .youtube_request import Filter, OptionalParameters, Part


class PlaylistPart(Part):
    part: list[str] = Field(
        default=['contentDetails', 'id', 'localizations', 'player', 'snippet', 'status']
    )


class PlaylistFilter(Filter):
    channelId: Optional[str] = ''
    mine: Optional[bool] = None


class PlaylistOptionalParameters(OptionalParameters):
    h1: Optional[str] = ''
    maxResults: Optional[int] = None
    onBehalfOfContentOwner: Optional[str] = ''
    onBehalfOfContentOwnerChannel: Optional[str] = ''
    pageToken: Optional[str] = ''


class CreatePlaylistSnippet(BaseModel):
    title: Optional[str] = ''
    description: Optional[str] = ''
    defaultLanguage: Optional[str] = ''


class CreateStatus(BaseModel):
    privacyStatus: str


class CreatePlaylist(BaseModel):
    snippet: CreatePlaylistSnippet
    status: Optional[CreateStatus] = None
