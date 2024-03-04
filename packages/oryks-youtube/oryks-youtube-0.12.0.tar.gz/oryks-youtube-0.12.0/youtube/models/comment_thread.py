from typing import Optional

from pydantic import BaseModel, Field

from .comment import Comment
from .resource import Resource


class Snippet(BaseModel):
    channel_id: str
    video_id: str
    top_level_comment: Comment
    can_reply: bool
    total_reply_count: int
    is_public: bool


class CommentThread(Resource):
    id: str
    snippet: Snippet
    replies: list[Comment] = Field(default_factory=list)
