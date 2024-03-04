from pydantic import BaseModel, Field

from ..models.resource import Resource


class YouTubeListResponse(BaseModel):
    kind: str
    etag: str
    items: list[Resource] = Field(default_factory=list)
