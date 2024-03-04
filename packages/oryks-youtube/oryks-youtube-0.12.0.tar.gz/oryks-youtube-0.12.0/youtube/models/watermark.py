from enum import Enum, auto

from pydantic import BaseModel


class TimingType(Enum):
    OffsetFromStart = auto()
    OffsetFromEnd = auto()


class WaterMark(BaseModel):
    timing_type: TimingType
    offset_ms: int
    duration_ms: int
    position_type: str
    corner_position: str
    image_url: str
    image_bytes: bytes
    target_channel_id: str
