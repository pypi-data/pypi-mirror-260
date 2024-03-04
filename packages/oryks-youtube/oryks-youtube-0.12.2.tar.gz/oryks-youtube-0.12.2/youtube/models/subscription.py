from pydantic import BaseModel

from .content_details import BaseContentDetails
from .resource import Resource
from .resource_id import ResourceId
from .snippet import BaseSnippet
from .thumbnail import Thumbnail


class SubscriptionSnippet(BaseSnippet):
    channel_title: str
    channel_id: str
    resource_id: ResourceId


class SubscriptionContentDetails(BaseContentDetails):
    total_item_count: int
    new_item_count: int
    activity_type: str


class SubscriberSnippet(BaseModel):
    title: str
    description: str
    channel_id: str
    thumbnails: Thumbnail


class Subscription(Resource):
    snippet: SubscriptionSnippet
    content_details: SubscriptionContentDetails
    subscriber_snippet: SubscriberSnippet
