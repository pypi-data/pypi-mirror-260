from pydantic import BaseModel


class Localization(BaseModel):
    title: str
    description: str
