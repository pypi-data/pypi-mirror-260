from datetime import datetime
from typing import Optional

from pydantic import Field

from .youtube_request import Filter, OptionalParameters, Part


class ActivityPart(Part):
    part: list[str] = Field(default=['contentDetails', 'id', 'snippet'])


class ActivityFilter(Filter):
    channelId: Optional[str] = None
    mine: Optional[bool] = None


class ActivityOptionalParameters(OptionalParameters):
    regionCode: Optional[str] = None
    publishedAfter: Optional[datetime] = None
    publishedBefore: Optional[datetime] = None
    pageToken: Optional[str] = None
    maxResults: Optional[int] = None
