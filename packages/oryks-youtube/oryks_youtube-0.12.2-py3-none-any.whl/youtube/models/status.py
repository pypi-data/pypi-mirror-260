from pydantic import BaseModel


class Status(BaseModel):
    privacy_status: str


class BaseStatus(BaseModel):
    privacy_status: str
