from abc import ABC

from pydantic import BaseModel


class ResourceSchema(ABC, BaseModel):
    pass


class Resource(ABC, BaseModel):
    pass
