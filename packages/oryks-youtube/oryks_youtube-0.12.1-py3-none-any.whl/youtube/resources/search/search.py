from datetime import datetime
from typing import Any, Iterator

from ...models import BaseSnippet, ResourceType, Search
from ...schemas import (
    PageInfo,
    SearchFilter,
    SearchOptionalParameters,
    SearchPart,
    YouTubeRequest,
    YouTubeResponse,
)
from ..resource import YouTubeResource


class YouTubeSearch(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)
        self.search_schema: YouTubeRequest = None
        self.next_page_token: str = None

    def parse_id(self, id_data: dict[str, str]) -> dict[str, str]:
        resource_id: str = ''
        resource_type: ResourceType = None
        if id_data['kind'] == 'youtube#playlist':
            resource_id = id_data['playlistId']
            resource_type = 'playlist'
        elif id_data['kind'] == 'youtube#video':
            resource_id = id_data['videoId']
            resource_type = 'video'
        else:
            resource_id = id_data['channelId']
            resource_type = 'channel'
        parsed_id_data: dict[str, str] = {
            'resource_id': resource_id,
            'resource_type': resource_type,
        }
        return parsed_id_data

    def parse_snippet(
        self, snippet_data: dict[str, str | datetime]
    ) -> dict[str, str | datetime]:
        base_snippet: BaseSnippet = self.parse_base_snippet(snippet_data)
        parsed_snippet: dict[str, Any] = base_snippet.model_dump()
        parsed_snippet['channel_id'] = snippet_data['channelId']
        parsed_snippet['channel_title'] = snippet_data['channelTitle']
        parsed_snippet['live_broadcast_content'] = snippet_data['liveBroadcastContent']
        parsed_snippet['publish_time'] = snippet_data['publishTime']
        return parsed_snippet

    def parse_item(self, item: dict) -> Search:
        id_data: dict = self.parse_id(item['id'])
        snippet_data: dict = self.parse_snippet(item['snippet'])
        parsed_item: Search = Search(
            resource_id=id_data['resource_id'],
            resource_type=id_data['resource_type'],
            description=snippet_data['description'],
            thumbnails=snippet_data['thumbnails'],
            title=snippet_data['title'],
            channel_id=snippet_data['channel_id'],
            published_at=snippet_data['published_at'],
            channel_title=snippet_data['channel_title'],
            live_broadcast_content=snippet_data['live_broadcast_content'],
            publish_time=snippet_data['publish_time'],
        )
        return parsed_item

    def search(self, search_schema: YouTubeRequest) -> YouTubeResponse:
        search_dict: dict[str, Any] = self.create_request_dict(search_schema)
        search_request = self.youtube_client.search().list(**search_dict)
        search_response = search_request.execute()
        return self.parse_youtube_response(search_response)

    def find_channel_by_name(self, display_name: str) -> str:
        part: SearchPart = SearchPart()
        optional_parameters: SearchOptionalParameters = SearchOptionalParameters(
            q=display_name, type=['channel']
        )
        search_request: YouTubeRequest = YouTubeRequest(
            part=part, optional_parameters=optional_parameters
        )
        return self.search(search_request)

    def __iter__(self):
        return self

    def __next__(self) -> list[Search]:
        self.search_schema.optional_parameters.pageToken = self.next_page_token
        search_results: YouTubeResponse = self.search(self.search_schema)
        self.next_page_token = search_results.nextPageToken
        return search_results.items

    def get_search_iterator(self, search_schema: YouTubeResponse) -> Iterator:
        self.search_schema = search_schema
        return self
