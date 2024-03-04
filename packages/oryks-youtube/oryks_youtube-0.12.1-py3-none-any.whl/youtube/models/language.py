from pydantic import BaseModel

from .resource import Resource


class LanguageSnippet(BaseModel):
    hl: str
    name: str


class Language(Resource):
    snippet: LanguageSnippet
