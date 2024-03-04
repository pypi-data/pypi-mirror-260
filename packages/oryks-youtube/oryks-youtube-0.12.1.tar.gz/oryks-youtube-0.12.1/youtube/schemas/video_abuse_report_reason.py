from typing import Optional

from pydantic import BaseModel


class VideoReportReasonSchema(BaseModel):
    videoId: str
    reasomId: str
    secondaryReasonId: Optional[str] = None
    comments: Optional[str] = None
    language: Optional[str] = None
