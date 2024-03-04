from typing import Optional

from pydantic import BaseModel

from .snippet import BaseSnippet


class Resource(BaseModel):
    id: Optional[str] = None
    snippet: Optional[BaseSnippet] = None
