from enum import Enum, auto

from pydantic import BaseModel

from .resource_type import ResourceType


class Activities(Enum):
    channelItem = 'channelItem'
    comment = 'comment'
    favorite = 'favorite'
    like = 'like'
    playlistItem = 'playlistItem'
    promotedItem = 'promotedItem'
    recommendation = 'recommendation'
    social = 'social'
    subscription = 'subscription'
    upload = 'upload'
    bulletin = 'bulletin'


class ResourceId(BaseModel):
    kind: str
    id: str


class ActivityType(BaseModel):
    pass


class VideoUploaded(ActivityType):
    video_id: str


class VideoLiked(ActivityType):
    resource_id: ResourceId


class VideoAddedToFavorite(ActivityType):
    resource_id: ResourceId


class CommentAdded(ActivityType):
    resource_id: ResourceId


class UserSubscribedToChannel(ActivityType):
    resource_id: ResourceId


class VideoAddedToPlaylist(ActivityType):
    video_id: str
    playlist_id: str


class Reccomendation(ActivityType):
    resource_id: ResourceId
    reason: str
    seed_resource_id: ResourceId


class ShareToSocial(ActivityType):
    type: str
    resource_id: ResourceId
    author: str
    reference_url: str
    image_url: str


class ChannelItem(ActivityType):
    resource_id: ResourceId


class PromotedItem(ActivityType):
    pass


class Bulletin(ActivityType):
    pass
