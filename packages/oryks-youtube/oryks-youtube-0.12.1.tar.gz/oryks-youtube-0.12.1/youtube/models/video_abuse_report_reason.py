from pydantic import BaseModel

from .resource import Resource


class VideoAbuseReportReasonSnippet(BaseModel):
    label: str


class VideoAbuseReportReason(Resource):
    snippet: VideoAbuseReportReasonSnippet
