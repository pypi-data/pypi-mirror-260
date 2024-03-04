from pydantic import BaseModel


class ResourceId(BaseModel):
    id: str
    kind: str
