from typing import Any

from ...models import BaseContentDetails, BaseSnippet, PlaylistItem
from ...schemas import (
    CreatePlaylistItem,
    PlaylistItemFilter,
    PlaylistItemOptionalParameters,
    PlaylistItemPart,
    YouTubeListResponse,
    YouTubeRequest,
    YouTubeResponse,
)
from ..resource import YouTubeResource


class YouTubePlaylistItem(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)

    def parse_resource_id(self, resource_id: dict) -> dict:
        parsed_resource_id: dict = dict()
        if resource_id.get('videoId'):
            parsed_resource_id['id'] = resource_id['videoId']
        elif resource_id.get('channelId'):
            parsed_resource_id['id'] = resource_id['channelId']
        else:
            parsed_resource_id['id'] = resource_id['playlistId']
        parsed_resource_id['kind'] = resource_id['kind']
        return parsed_resource_id

    def parse_snippet(self, snippet_data: dict[str, Any]) -> dict[str, Any]:
        base_snippet: BaseSnippet = self.parse_base_snippet(snippet_data)
        parsed_snippet: dict[str, Any] = base_snippet.model_dump()
        parsed_snippet['channel_id'] = snippet_data['channelId']
        parsed_snippet['channel_title'] = snippet_data['channelTitle']
        if snippet_data.get('videoOwnerChannelTitle'):
            parsed_snippet['video_owner_channel_title'] = snippet_data[
                'videoOwnerChannelTitle'
            ]
        if snippet_data.get('videoOwnerChannelTitle'):
            parsed_snippet['video_owner_channel_id'] = snippet_data[
                'videoOwnerChannelTitle'
            ]
        if snippet_data.get('playlistId'):
            parsed_snippet['playlist_id'] = snippet_data['playlistId']
        if snippet_data.get('position'):
            parsed_snippet['position'] = snippet_data['position']
        if snippet_data.get('playlistId'):
            parsed_snippet['resource_id'] = self.parse_resource_id(
                snippet_data['resourceId']
            )
        return dict(snippet=parsed_snippet)

    def parse_content_details(self, content_details: dict) -> dict:
        base_content_details: BaseContentDetails = self.parse_base_content_details(
            content_details
        )
        parsed_content_details: dict = base_content_details.model_dump()
        parsed_content_details['video_id'] = content_details['videoId']
        if content_details.get('note'):
            parsed_content_details['note'] = content_details['note']
        if content_details.get('videoPublishedAt'):
            parsed_content_details['video_published_at'] = content_details[
                'videoPublishedAt'
            ]
        return dict(content_details=parsed_content_details)

    def parse_item(self, item: dict) -> PlaylistItem:
        id_data: dict = self.parse_id(item)
        if item.get('snippet'):
            snippet_data: dict = self.parse_snippet(item['snippet'])
            id_data.update(snippet_data)
        if item.get('contentDetails'):
            content_details: dict = self.parse_content_details(item['contentDetails'])
            id_data.update(content_details)
        return PlaylistItem(**id_data)

    def find_playlist_items(
        self, playlist_id: str, max_results: int
    ) -> YouTubeResponse:
        part: PlaylistItemPart = PlaylistItemPart()
        optional_params: PlaylistItemOptionalParameters = (
            PlaylistItemOptionalParameters(maxResults=max_results)
        )
        request_filter: PlaylistItemFilter = PlaylistItemFilter(playlistId=playlist_id)
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part, filter=request_filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(request_schema)
        find_items_request: dict = self.youtube_client.playlistItems().list(
            **request_dict
        )
        find_items_result: dict = find_items_request.execute()
        return self.parse_youtube_response(find_items_result)

    def find_playlist_items_by_ids(
        self, playlist_item_ids: list[str]
    ) -> YouTubeListResponse:
        request_filter: PlaylistItemFilter = PlaylistItemFilter(id=playlist_item_ids)
        part: PlaylistItemPart = PlaylistItemPart()
        optional_params: PlaylistItemOptionalParameters = (
            PlaylistItemOptionalParameters()
        )
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part, filter=request_filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(request_schema)
        find_video_request: dict = self.youtube_client.playlistItems().list(
            **request_dict
        )
        find_video_result: dict[str, int | str] = find_video_request.execute()
        return self.parse_youtube_list_response(find_video_result)

    def insert_playlist_item(self, create_item: CreatePlaylistItem) -> PlaylistItem:
        insert_playlist_item_request: dict = self.youtube_client.playlistItems().insert(
            part='snippet', body=create_item.model_dump()
        )
        insert_playlist_item_response = insert_playlist_item_request.execute()
        return self.parse_item(insert_playlist_item_response)

    def update_playlist_item(
        self, playlist_id: str, playlist_item_id: str, video_id: str, position: int = 1
    ) -> PlaylistItem:
        update_playlist_item_request: dict = self.youtube_client.playlistItems().update(
            part='snippet',
            body={
                'id': playlist_item_id,
                'snippet': {
                    'playlistId': playlist_id,
                    'position': position,
                    'resourceId': {'kind': 'youtube#video', 'videoId': video_id},
                },
            },
        )
        update_playlist_item_response = update_playlist_item_request.execute()
        return self.parse_item(update_playlist_item_response)

    def delete_playlist_item(self, playlist_item_id: str) -> None:
        delete_playlist_item_request: dict = self.youtube_client.playlistItems().delete(
            id=playlist_item_id,
        )
        delete_playlist_item_request.execute()
