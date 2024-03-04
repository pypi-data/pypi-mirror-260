from datetime import datetime
from enum import Enum, auto

from pydantic import BaseModel


class TrackKind(Enum):
    Asr = auto()
    Forced = auto()
    Standard = auto()


class AudioTrackType(Enum):
    Commentary = auto()
    Descriptive = auto()
    Primary = auto()
    Unknown = auto()


class Status(Enum):
    Failed = auto()
    Serving = auto()
    Syncing = auto()


class FailureReason(Enum):
    ProcessingFailed = auto()
    UnknownFormat = auto()
    UnsupportedFormat = auto()


class Caption(BaseModel):
    video_id: str
    last_updated: datetime
    track_kind: TrackKind
    language: str
    name: str
    audio_track_type: str
    is_cc: bool
    is_large: bool
    is_easy_reader: bool
    is_draft: bool
    is_auto_synced: bool
    status: str
    failure_reason: str
