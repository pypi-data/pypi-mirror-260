from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .resource import Resource


class Author(BaseModel):
    display_name: str
    profile_image_url: str
    channel_url: Optional[str] = ''
    channel_id: Optional[str] = ''


class CommentSnippet(BaseModel):
    author: Author
    channel_id: str
    text_display: str
    text_original: str
    can_rate: bool
    viewer_rating: str
    like_count: int
    # moderation_status: str
    published_at: datetime
    updated_at: datetime
    video_id: Optional[str] = None
    parent_id: Optional[str] = None


class Comment(Resource):
    id: str
    snippet: CommentSnippet
