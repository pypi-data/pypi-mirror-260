from pydantic import BaseModel

from ..models.rating import YouTubeVideoRating


class YouTubeRatingResponse(BaseModel):
    kind: str
    etag: str
    items: list[YouTubeVideoRating]
