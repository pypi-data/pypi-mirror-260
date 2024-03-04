from datetime import datetime

from pydantic import BaseModel

from .localized import Localized
from .thumbnail import Thumbnail


class BaseSnippet(BaseModel):
    title: str
    description: str
    thumbnails: Thumbnail
    published_at: datetime
