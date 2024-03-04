from typing import Optional

from .youtube_list_response import YouTubeListResponse


class YouTubeResponse(YouTubeListResponse):
    nextPageToken: Optional[str] = ''
    prevPageToken: Optional[str] = ''
