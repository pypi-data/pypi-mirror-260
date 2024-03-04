from typing import Optional

from pydantic import BaseModel, Field

from .youtube_request import Filter, OptionalParameters, Part


class CommentThreadPart(Part, BaseModel):
    part: list[str] = Field(default=['id', 'replies', 'snippet'])


class CommentThreadFilter(Filter, BaseModel):
    allThreadsRelatedToChannelId: Optional[str] = ''
    id: Optional[list[str]] = Field(default_factory=list)
    channelId: Optional[str] = None
    videoId: Optional[str] = None


class CommentThreadOptionalParameters(OptionalParameters):
    maxResults: Optional[int] = None
    moderationStatus: Optional[int] = None
    order: Optional[str] = None
    pageToken: Optional[str] = None
    searchTerms: Optional[list[str]] = Field(default_factory=list)
    textFormat: Optional[str] = None
