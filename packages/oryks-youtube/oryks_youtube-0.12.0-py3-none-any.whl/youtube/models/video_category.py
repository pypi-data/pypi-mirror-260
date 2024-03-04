from pydantic import BaseModel

from .resource import Resource


class VideoCategorySnippet(BaseModel):
    title: str
    assignable: bool
    channel_id: str


class VideoCategory(Resource):
    id: str
    snippet: VideoCategorySnippet
