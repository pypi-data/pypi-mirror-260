from typing import Optional

from pydantic import BaseModel, Field

from .youtube_request import Filter, OptionalParameters, Part


class ChannelSectionPart(Part):
    part: list[str] = Field(default=['contentDetails', 'id', 'snippet'])


class ChannelSectionFilter(Filter):
    channelId: Optional[str] = None
    id: Optional[str] = None
    mine: Optional[bool] = None


class ChannelSectionOptionalParameters(OptionalParameters):
    onBehalfOfContentOwner: Optional[str] = None


class InsertChannelSectionSnippet(BaseModel):
    type: str
    title: Optional[str] = None
    position: Optional[int] = None


class InsertChannelSectionContentDetails(BaseModel):
    playlists: list[str] = Field(default_factory=list)
    channels: list[str] = Field(default_factory=list)


class InsertChannelSection(BaseModel):
    snippet: InsertChannelSectionSnippet
    content_details: Optional[InsertChannelSectionContentDetails] = None
