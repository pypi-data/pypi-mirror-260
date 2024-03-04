from typing import Any

from ...models import (
    Activities,
    Activity,
    ActivityContentDetails,
    ActivitySnippet,
    ActivityType,
    Bulletin,
    ChannelItem,
    CommentAdded,
    PromotedItem,
    Reccomendation,
    ResourceId,
    ShareToSocial,
    UserSubscribedToChannel,
    VideoAddedToFavorite,
    VideoAddedToPlaylist,
    VideoLiked,
    VideoUploaded,
)
from ...schemas import (
    ActivityFilter,
    ActivityOptionalParameters,
    ActivityPart,
    YouTubeRequest,
    YouTubeResponse,
    YouTubeListResponse
)
from ..resource import YouTubeResource


class YouTubeActivity(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)

    def list_channel_activity(self, request: YouTubeRequest) -> YouTubeResponse:
        raise NotImplementedError()

    def list_my_activities(self) -> YouTubeListResponse:
        actvities_request = self.youtube_client.activities().list(
            part='id,snippet,contentDetails', maxResults=25, mine=True
        )
        actvities_response = actvities_request.execute()
        return actvities_response

    def parse_snippet(self, snippet_data: dict[str, Any]) -> ActivitySnippet:
        snippet: dict = dict(**self.parse_base_snippet(snippet_data).model_dump())
        snippet['channel_id'] = snippet_data['channelId']
        snippet['channel_title'] = snippet_data['channelTitle']
        snippet['type'] = snippet_data['type']
        if snippet_data.get('groupId'):
            snippet['group_id'] = snippet_data['groupId']
        else:
            snippet['group_id'] = None
        return ActivitySnippet(**snippet)

    def parse_activity_type(
        self, content_details: dict, activities_type: str
    ) -> ActivityType:
        activity_type: ActivityType = None
        if activities_type == Activities.playlistItem.value:
            activity_type = VideoAddedToPlaylist(
                video_id=content_details['playlistItem']['resourceId']['videoId'],
                playlist_id=content_details['playlistItem']['playlistId'],
            )
        elif activities_type == Activities.channelItem.value:
            activity_type = ChannelItem(
                resource_id=ResourceId(
                    kind=content_details['recommendation']['resourceId']['kind'],
                    id=content_details['recommendation']['resourceId']['channelId'],
                )
            )
        elif activities_type == Activities.comment.value:
            id: str = None
            kind = content_details['comment']['resourceId']['kind']
            if kind == 'youtube#video':
                id = 'videoId'
            elif kind == 'youtube#channel':
                id = 'channelId'
            activity_type = CommentAdded(
                resource_id=ResourceId(
                    kind=kind, id=content_details['recommendation']['resourceId'][id]
                )
            )
        elif activities_type == Activities.favorite.value:
            activity_type = VideoAddedToFavorite(
                resource_id=ResourceId(
                    kind=content_details['recommendation']['resourceId']['kind'],
                    id=content_details['recommendation']['resourceId']['videoId'],
                )
            )
        elif activities_type == Activities.like.value:
            activity_type = VideoLiked(
                resource_id=ResourceId(
                    kind=content_details['recommendation']['resourceId']['kind'],
                    id=content_details['recommendation']['resourceId']['videoId'],
                )
            )
        elif activities_type == Activities.promotedItem.value:
            activity_type = PromotedItem()
        elif activities_type == Activities.recommendation.value:
            activity_type = Reccomendation(
                reason='',
                resource_id=ResourceId(kind='', id=''),
                seed_resource_id=ResourceId(kind='', id=''),
            )
        elif activities_type == Activities.social.value:
            activity_type = ShareToSocial(
                type='',
                resource_id=ResourceId(kind='', id=''),
                author='',
                reference_url='',
                image_url='',
            )
        elif activities_type == Activities.subscription.value:
            activity_type = UserSubscribedToChannel(
                resource_id=ResourceId(
                    kind=content_details['recommendation']['resourceId']['kind'],
                    id=content_details['recommendation']['resourceId']['channelId'],
                )
            )
        elif activities_type == Activities.upload.value:
            activity_type = VideoUploaded(video_id='')
        elif activities_type == Activities.bulletin.value:
            activity_type = Bulletin()
        else:
            activity_type = ActivityType()
        return activity_type

    def parse_content_details(
        self, content_details_data: dict, activities_type: str
    ) -> ActivityContentDetails:
        content_details: dict = dict(
            **self.parse_base_content_details(content_details_data).model_dump()
        )
        content_details['activity_type'] = self.parse_activity_type(
            content_details=content_details_data, activities_type=activities_type
        )
        return ActivityContentDetails(**content_details)

    def parse_item(self, item: dict) -> Activity:
        activity_data: dict = dict()
        activity_data.update(self.parse_id(item))
        activity_data.update(dict(snippet=self.parse_snippet(item['snippet'])))
        activity_data.update(
            dict(
                content_details=self.parse_content_details(
                    content_details_data=item['contentDetails'],
                    activities_type=item['snippet']['type'],
                )
            )
        )
        activity: Activity = Activity(**activity_data)
        return activity

    def parse_items(self, activity_items: list[Activity]):
        parsed_activity_items: list[Activity] = [
            self.parse_item(activity_item) for activity_item in activity_items
        ]
        return parsed_activity_items
