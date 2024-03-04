from typing import Optional

from pydantic import BaseModel


class VideoReportAbuse(BaseModel):
    video_id: str
    reason_id: str
    secondary_reason_id: Optional[str] = None
    comments: Optional[str] = None
    language: Optional[str] = None
