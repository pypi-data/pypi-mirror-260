from typing import Any

from ...models import (
    Channel,
    ChannelContentDetails,
    ChannelSnippet,
    ChannelStatistics,
    ChannelStatus,
)
from ...schemas import (
    ChannelFilter,
    ChannelOptionalParameters,
    ChannelPart,
    YouTubeListResponse,
    YouTubeRequest,
)
from ..resource import YouTubeResource


class YouTubeChannel(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)

    def parse_snippet(self, snippet_data: dict[str, Any]) -> ChannelSnippet:
        snippet: dict = dict(**self.parse_base_snippet(snippet_data).model_dump())
        snippet['custom_url'] = snippet_data['customUrl']
        snippet['country'] = snippet_data.get('country', '')
        snippet['localized'] = self.parse_localizations(snippet_data['localized'])
        return ChannelSnippet(**snippet)

    def parse_content_details(
        self, content_details_data: dict
    ) -> ChannelContentDetails:
        content_details: dict = dict(
            **self.parse_base_content_details(content_details_data).model_dump()
        )
        content_details['related_playlists'] = content_details_data['relatedPlaylists']
        return ChannelContentDetails(**content_details)

    def parse_statistics(self, statistics_data: dict) -> ChannelStatistics:
        statistics: dict[str, int | bool] = dict()
        statistics['views_count'] = statistics_data['viewCount']
        statistics['subscribers_count'] = statistics_data['subscriberCount']
        statistics['videos_count'] = statistics_data['videoCount']
        statistics['hidden_subscribers_count'] = statistics_data[
            'hiddenSubscriberCount'
        ]
        return ChannelStatistics(**statistics)

    def parse_status(self, status_data: dict) -> ChannelStatus:
        status: dict = dict(**self.parse_base_status(status_data).model_dump())
        status['is_linked'] = status_data['isLinked']
        status['long_uploads_status'] = status_data['longUploadsStatus']
        status['made_for_kids'] = status_data.get('madeForKids', False)
        return ChannelStatus(**status)

    def parse_item(self, item: dict) -> Channel:
        channel_data: dict = dict()
        channel_data.update(self.parse_id(item))
        channel_data.update(dict(snippet=self.parse_snippet(item['snippet'])))
        channel_data.update(
            dict(content_details=self.parse_content_details(item['contentDetails']))
        )
        channel_data.update(dict(statistics=self.parse_statistics(item['statistics'])))
        channel_data.update(dict(status=self.parse_status(item['status'])))
        channel: Channel = Channel(**channel_data)
        return channel

    def find_channel_by_id(self, channel_id: str) -> YouTubeListResponse:
        request_filter: ChannelFilter = ChannelFilter(id=[channel_id])
        part: ChannelPart = ChannelPart()
        optional_params: ChannelOptionalParameters = ChannelOptionalParameters()
        youtube_request: YouTubeRequest = YouTubeRequest(
            part=part, filter=request_filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(youtube_request)
        find_channel_request: dict = self.youtube_client.channels().list(**request_dict)
        find_channel_result: dict[str, int | str] = find_channel_request.execute()
        return self.parse_youtube_list_response(find_channel_result)

    def find_channels_by_ids(self, channel_ids: list[str]) -> YouTubeListResponse:
        filter: ChannelFilter = ChannelFilter(id=channel_ids)
        part: ChannelPart = ChannelPart()
        optional_params: ChannelOptionalParameters = ChannelOptionalParameters()
        youtube_request: YouTubeRequest = YouTubeRequest(
            part=part, filter=filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(youtube_request)
        find_channel_request: dict = self.youtube_client.channels().list(**request_dict)
        find_channel_result: dict[str, int | str] = find_channel_request.execute()
        return self.parse_youtube_list_response(find_channel_result)

    def find_my_channel(self) -> YouTubeListResponse:
        filter: ChannelFilter = ChannelFilter(mine=True)
        part: ChannelPart = ChannelPart()
        optional_params: ChannelOptionalParameters = ChannelOptionalParameters()
        youtube_request: YouTubeRequest = YouTubeRequest(
            part=part, filter=filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(youtube_request)
        find_channel_request: dict = self.youtube_client.channels().list(**request_dict)
        find_channel_result: dict[str, int | str] = find_channel_request.execute()
        return self.parse_youtube_list_response(find_channel_result)
