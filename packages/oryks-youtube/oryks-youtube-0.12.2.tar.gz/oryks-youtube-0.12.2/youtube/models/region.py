from pydantic import BaseModel

from .resource import Resource


class RegionSnippet(BaseModel):
    gl: str
    name: str


class Region(Resource):
    snippet: RegionSnippet
