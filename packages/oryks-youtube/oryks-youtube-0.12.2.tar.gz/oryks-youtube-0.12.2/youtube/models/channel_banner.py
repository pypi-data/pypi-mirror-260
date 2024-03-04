from pydantic import BaseModel


class ChannelBanner(BaseModel):
    url: str
