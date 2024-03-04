from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')

from ..models import (
    BaseContentDetails,
    BaseSnippet,
    BaseStatus,
    Resource,
    Thumbnail,
    ThumbnailResolution,
)
from ..schemas import (
    Filter,
    OptionalParameters,
    PageInfo,
    Part,
    YouTubeListResponse,
    YouTubeRequest,
    YouTubeResponse,
)


class YouTubeResource(ABC):
    def __init__(self, youtube_client: Any) -> None:
        self.youtube_client: Any = youtube_client

    def generate_part(self, part: Part) -> str:
        """Generate the 'Part' for a request.

        Parameters
        ----------
        part: Part
            An instance of part that contains all the required details.
        """
        part_str: str = ','.join(part.part)
        return part_str

    def generate_optional_parameters(self, optional_params: OptionalParameters) -> dict:
        """Generate Optional parmateers for a request.

        Parameters
        ----------
        optional_parameters: OptionalParameters
            Optional parameters used when sending the request
        """
        optional: dict[str, Any] = dict()
        for key, value in optional_params.model_dump().items():
            #  We only want optional parameters that were provided
            if value:
                optional[key] = value
        #  This is useful when sending search request and type is provided as a list i.e ['video']
        if optional_params.model_dump().get('type'):
            optional['type'] = ','.join(optional_params.type)
        return optional

    def generate_filter(self, request_filter: Filter) -> dict[str, Any]:
        """Generate the filters for request to youtube."""
        #  We pick the very first filter.
        for key, value in request_filter.model_dump().items():
            if value:
                if key == 'id':
                    value: str = ','.join(value)
                return {key: value}
        return {}

    def create_request_dict(self, request_schema: YouTubeRequest) -> dict[str, Any]:
        """Create the request dict for sending request to youtube."""
        request_dict: dict[str, Any] = dict()
        request_dict['part'] = self.generate_part(request_schema.part)
        request_dict.update(
            self.generate_optional_parameters(request_schema.optional_parameters)
        )
        request_dict.update(self.generate_filter(request_schema.filter))
        return request_dict

    def parse_id(self, item: dict) -> dict:
        """Get the resource id from the youtube response."""
        return dict(id=item['id'])

    def parse_thumbnail(
        self, thumbnail_data: dict[str, int | str]
    ) -> ThumbnailResolution:
        """Parse a single thumbnail resolution.

        YouTube Thumbnails come in different resolutions e.g default, medium, high, standard
        """
        if not thumbnail_data:
            return None
        parsed_thumbnail: ThumbnailResolution = ThumbnailResolution(
            url=thumbnail_data.get('url', ''),
            width=thumbnail_data.get('width', 0),
            height=thumbnail_data.get('height', 0),
        )
        return parsed_thumbnail

    def parse_thumbnails(self, thumbnails_data: dict[str, int | str]) -> Thumbnail:
        """Parse all the thumbnails for a given resource."""
        parsed_thumbnail: Thumbnail = Thumbnail(
            default=self.parse_thumbnail(thumbnails_data.get('default', '')),
            medium=self.parse_thumbnail(thumbnails_data.get('medium', '')),
            high=self.parse_thumbnail(thumbnails_data.get('high', '')),
            standard=self.parse_thumbnail(thumbnails_data.get('standard', '')),
        )
        return parsed_thumbnail

    def parse_localizations(self, localized_details: dict) -> dict:
        """Parse localization details for a given resource."""
        parsed_localized: dict[str, str] = dict()
        parsed_localized['title'] = localized_details['title']
        parsed_localized['description'] = localized_details['description']
        return parsed_localized

    def parse_base_status(self, status: dict) -> BaseStatus:
        parsed_status: dict[str, str] = {}
        parsed_status['privacy_status'] = status['privacyStatus']
        return BaseStatus(**parsed_status)

    def parse_base_snippet(self, snippet_data: dict) -> BaseSnippet:
        parsed_snippet: dict[str, Any] = dict()
        parsed_snippet['published_at'] = snippet_data['publishedAt']
        parsed_snippet['title'] = snippet_data['title']
        parsed_snippet['description'] = snippet_data['description']
        parsed_snippet['thumbnails'] = self.parse_thumbnails(snippet_data['thumbnails'])
        return BaseSnippet(**parsed_snippet)

    def parse_base_content_details(self, content_details: dict) -> BaseContentDetails:
        return BaseContentDetails()

    @abstractmethod
    def parse_item(self, item: dict) -> Resource:
        pass

    def parse_items(self, items: list[dict]) -> list[Resource]:
        parsed_items: list[Resource] = [self.parse_item(item) for item in items]
        return parsed_items

    # Removed pageInfo=PageInfo(**youtube_list_response['pageInfo']),
    def parse_youtube_list_response(
        self, youtube_list_response: dict
    ) -> YouTubeListResponse:
        youtube_result: YouTubeListResponse = YouTubeListResponse(
            kind=youtube_list_response['kind'],
            etag=youtube_list_response['etag'],
            items=self.parse_items(youtube_list_response['items']),
        )
        return youtube_result

    def parse_youtube_response(self, youtube_response: dict) -> YouTubeResponse:
        youtube_result: YouTubeResponse = YouTubeResponse(
            kind=youtube_response['kind'],
            etag=youtube_response['etag'],
            pageInfo=PageInfo(**youtube_response['pageInfo']),
            items=self.parse_items(youtube_response['items']),
            nextPageToken=youtube_response.get('nextPageToken', ''),
            prevPageToken=youtube_response.get('prevPageToken', ''),
        )
        return youtube_result
