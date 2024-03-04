from typing import Any, Iterator

from ...models import BaseSnippet, Playlist
from ...schemas import (
    CreatePlaylist,
    PlaylistFilter,
    PlaylistOptionalParameters,
    PlaylistPart,
    YouTubeListResponse,
    YouTubeRequest,
    YouTubeResponse,
)
from ..resource import YouTubeResource


class YouTubePlaylist(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)
        self.my_playlists_schema: YouTubeRequest = None
        self.my_playlists_nxt_page_tkn: str = None

    def parse_snippet(self, snippet_data: dict[str, Any]) -> dict[str, Any]:
        base_snippet: BaseSnippet = self.parse_base_snippet(snippet_data)
        parsed_snippet: dict[str, Any] = base_snippet.model_dump()
        parsed_snippet['channel_id'] = snippet_data['channelId']
        parsed_snippet['channel_title'] = snippet_data['channelTitle']
        if snippet_data.get('defaultLanguage'):
            parsed_snippet['default_language'] = snippet_data['defaultLanguage']
        if snippet_data.get('localized'):
            parsed_snippet['localized'] = self.parse_localizations(
                snippet_data['localized']
            )
        if snippet_data.get('defaultAudioLanguage'):
            parsed_snippet['default_audio_language'] = snippet_data[
                'defaultAudioLanguage'
            ]
        return dict(snippet=parsed_snippet)

    def parse_status(self, status: dict) -> dict:
        parsed_status: dict[str, str] = {}
        parsed_status['privacy_status'] = status['privacyStatus']
        return dict(status=parsed_status)

    def parse_content_details(self, content_details: dict) -> dict:
        parsed_content_details: dict = dict()
        parsed_content_details['item_count'] = content_details['itemCount']
        return dict(content_details=parsed_content_details)

    def parse_item(self, item: dict) -> Playlist:
        id_data: dict = self.parse_id(item)
        if item.get('snippet'):
            snippet_data: dict = self.parse_snippet(item['snippet'])
            id_data.update(snippet_data)
        if item.get('contentDetails'):
            content_details: dict = self.parse_content_details(item['contentDetails'])
            id_data.update(content_details)
        if item.get('status'):
            status: dict = self.parse_status(item['status'])
            id_data.update(status)
        return Playlist(**id_data)

    def find_channel_playlists(
        self, channel_id: str, max_result: int = 25
    ) -> YouTubeListResponse:
        part: PlaylistPart = PlaylistPart()
        request_filter: PlaylistFilter = PlaylistFilter(channelId=channel_id)
        optional_params: PlaylistOptionalParameters = PlaylistOptionalParameters(
            maxResults=max_result
        )
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part, filter=request_filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(request_schema)
        find_channel_playlist_request: dict = self.youtube_client.playlists().list(
            **request_dict
        )
        find_channel_playlist_result: dict[
            str, int | str
        ] = find_channel_playlist_request.execute()
        return self.parse_youtube_list_response(find_channel_playlist_result)

    def find_my_playlists(self, max_result: int = 25) -> YouTubeListResponse:
        part: PlaylistPart = PlaylistPart()
        request_filter: PlaylistFilter = PlaylistFilter(mine=True)
        optional_params: PlaylistOptionalParameters = PlaylistOptionalParameters(
            maxResults=max_result
        )
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part,
            optional_parameters=optional_params,
            filter=request_filter,
        )
        request_dict = self.create_request_dict(request_schema)
        find_channel_playlist_request: dict = self.youtube_client.playlists().list(
            **request_dict
        )
        find_channel_playlist_result: dict[
            str, int | str
        ] = find_channel_playlist_request.execute()
        return self.parse_youtube_response(find_channel_playlist_result)

    def insert_playlist(self, playlist_schema: CreatePlaylist) -> Playlist:
        create_playlist_req = self.youtube_client.playlists().insert(
            part=','.join(playlist_schema.model_dump().keys()),
            body=playlist_schema.model_dump(),
        )
        create_playlist_resp = create_playlist_req.execute()
        return self.parse_item(create_playlist_resp)

    def update_playlist(
        self, playlist_id: str, playlist_schema: CreatePlaylist
    ) -> Playlist:
        request_dict: dict = dict(id=playlist_id)
        request_dict.update(playlist_schema.model_dump())
        update_playlist_req = self.youtube_client.playlists().update(
            part=','.join(playlist_schema.model_dump().keys()), body=request_dict
        )
        update_playlist_resp = update_playlist_req.execute()
        return self.parse_item(update_playlist_resp)

    def delete_playlist(self, playlist_id: str) -> None:
        delete_playlist_req = self.youtube_client.playlists().delete(id=playlist_id)
        delete_playlist_req.execute()

    def __iter__(self):
        return self

    def __next__(self) -> list[Playlist]:
        self.my_playlists_schema.optional_parameters.pageToken = (
            self.my_playlists_nxt_page_tkn
        )
        request_dict = self.create_request_dict(self.my_playlists_schema)
        find_channel_playlist_request: dict = self.youtube_client.playlists().list(
            **request_dict
        )
        find_channel_resp: dict = find_channel_playlist_request.execute()
        find_channel_playlist_result: YouTubeResponse = self.parse_youtube_response(
            find_channel_resp
        )
        self.my_playlists_nxt_page_tkn = find_channel_playlist_result.nextPageToken
        if not self.my_playlists_nxt_page_tkn:
            raise StopIteration()
        return find_channel_playlist_result.items

    def get_my_playlists_iterator(self, max_results: int = 10) -> Iterator:
        part: PlaylistPart = PlaylistPart()
        request_filter: PlaylistFilter = PlaylistFilter(mine=True)
        optional_params: PlaylistOptionalParameters = PlaylistOptionalParameters(
            maxResults=max_results
        )
        self.my_playlists_schema = YouTubeRequest(
            part=part,
            optional_parameters=optional_params,
            filter=request_filter,
        )
        return self
