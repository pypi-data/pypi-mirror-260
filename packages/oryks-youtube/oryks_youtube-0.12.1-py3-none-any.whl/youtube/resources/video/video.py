from collections import defaultdict
from typing import Any

from googleapiclient.http import MediaFileUpload

from ...models import (
    BaseContentDetails,
    BaseSnippet,
    Language,
    LanguageSnippet,
    Region,
    RegionSnippet,
    Video,
    VideoAbuseReportReason,
    VideoAbuseReportReasonSnippet,
    VideoCategory,
    VideoCategorySnippet,
)
from ...schemas import (
    UploadVideo,
    VideoFilter,
    VideoOptionalParameters,
    VideoPart,
    VideoReportReasonSchema,
    YouTubeListResponse,
    YouTubeRatingResponse,
    YouTubeRequest,
)
from ..resource import YouTubeResource


class YouTubeVideo(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)

    def parse_snippet(self, snippet_data: dict[str, Any]) -> dict[str, Any]:
        base_snippet: BaseSnippet = self.parse_base_snippet(snippet_data)
        parsed_snippet: dict[str, Any] = base_snippet.model_dump()
        parsed_snippet['channel_id'] = snippet_data['channelId']
        parsed_snippet['channel_title'] = snippet_data['channelTitle']
        parsed_snippet['live_broadcast_content'] = snippet_data['liveBroadcastContent']
        if snippet_data.get('tags'):
            parsed_snippet['tags'] = snippet_data['tags']
        parsed_snippet['category_id'] = snippet_data['categoryId']
        if snippet_data.get('defaultLanguage'):
            parsed_snippet['default_language'] = snippet_data['defaultLanguage']
        parsed_snippet['localized'] = self.parse_localizations(
            snippet_data['localized']
        )
        if snippet_data.get('defaultAudioLanguage'):
            parsed_snippet['default_audio_language'] = snippet_data[
                'defaultAudioLanguage'
            ]
        return dict(snippet=parsed_snippet)

    def parse_statistics(self, statistics: dict) -> dict:
        parsed_statistics: dict[str, int] = dict()
        parsed_statistics['views_count'] = statistics['viewCount']
        parsed_statistics['likes_count'] = statistics['likeCount']
        parsed_statistics['comments_count'] = statistics['commentCount']
        return dict(statistics=parsed_statistics)

    def parse_region_restriction(self, region_restriction: dict) -> dict:
        parsed_region_restriction: dict[str, list[str]] = dict()
        if region_restriction.get('allowed'):
            parsed_region_restriction['allowed'] = region_restriction.get('allowed')
        else:
            parsed_region_restriction['allowed'] = []
        if region_restriction.get('blocked'):
            parsed_region_restriction['blocked'] = region_restriction.get('blocked')
        else:
            parsed_region_restriction['blocked'] = []
        return dict(region_restriction=parsed_region_restriction)

    def parse_content_details(self, content_details: dict) -> dict:
        base_content_details: BaseContentDetails = self.parse_base_content_details(
            content_details
        )
        parsed_content_details: dict = base_content_details.model_dump()
        parsed_content_details['duration'] = content_details['duration']
        parsed_content_details['dimension'] = content_details['dimension']
        parsed_content_details['definition'] = content_details['definition']
        parsed_content_details['caption'] = content_details['caption']
        parsed_content_details['licensed_content'] = content_details['licensedContent']
        if content_details.get('regionRestriction'):
            parsed_content_details[
                'region_restriction'
            ] = self.parse_region_restriction(content_details['regionRestriction'])
        parsed_content_details['projection'] = content_details['projection']
        if content_details.get('hasCustomThumbnail'):
            parsed_content_details['has_custom_thumbnail'] = content_details[
                'hasCustomThumbnail'
            ]
        return dict(content_details=parsed_content_details)

    def parse_youtube_rating(self, rating_data: dict) -> dict:
        raise NotImplementedError()

    def parse_file_details(self, content_details: dict) -> dict:
        raise NotImplementedError()

    def parse_live_streaming_details(self, content_details: dict) -> dict:
        raise NotImplementedError()

    def parse_player(self, content_details: dict) -> dict:
        raise NotImplementedError()

    def parse_processing_details(self, content_details: dict) -> dict:
        raise NotImplementedError()

    def parse_recording_details(self, content_details: dict) -> dict:
        raise NotImplementedError()

    def parse_status(self, status: dict) -> dict:
        raise NotImplementedError()

    def parse_suggestions(self, suggestions: dict) -> dict:
        raise NotImplementedError()

    def parse_topic_details(self, topic_details: dict) -> dict:
        raise NotImplementedError()

    def parse_user_video_rating(self, rating_response: dict) -> YouTubeListResponse:
        print(rating_response)
        video_ratings: list[dict[str, str]] = [
            {'video_id': rating['videoId'], 'rating': rating['rating']}
            for rating in rating_response['items']
        ]
        rating_response: YouTubeListResponse = YouTubeListResponse(
            etag=rating_response['etag'],
            kind=rating_response['kind'],
            items=video_ratings,
        )
        return rating_response

    def parse_video_categories(
        self, video_categorie_response: dict[str, Any]
    ) -> YouTubeListResponse:
        categories: list[VideoCategory] = [
            VideoCategory(
                id=category['id'],
                snippet=VideoCategorySnippet(
                    title=category['snippet']['title'],
                    assignable=category['snippet']['assignable'],
                    channel_id=category['snippet']['channelId'],
                ),
            )
            for category in video_categorie_response['items']
        ]
        response: YouTubeListResponse = YouTubeListResponse(
            kind=video_categorie_response['kind'],
            etag=video_categorie_response['etag'],
            items=categories,
        )
        return response

    def parse_video_abuse_report_reasons(
        self, video_abuse_report_reasons: dict
    ) -> YouTubeListResponse:
        abuse_reasons: list[VideoAbuseReportReasonSnippet] = [
            VideoAbuseReportReason(
                id=reason['id'],
                snippet=VideoAbuseReportReasonSnippet(label=reason['snippet']['label']),
            )
            for reason in video_abuse_report_reasons['items']
        ]
        response: YouTubeListResponse = YouTubeListResponse(
            kind=video_abuse_report_reasons['kind'],
            etag=video_abuse_report_reasons['etag'],
            items=abuse_reasons,
        )
        return response

    def parse_languages_response(self, languages_response: dict) -> YouTubeListResponse:
        languages: list[Language] = [
            Language(
                id=language['id'],
                snippet=LanguageSnippet(
                    hl=language['snippet']['hl'], name=language['snippet']['name']
                ),
            )
            for language in languages_response['items']
        ]
        response: YouTubeListResponse = YouTubeListResponse(
            kind=languages_response['kind'],
            etag=languages_response['etag'],
            items=languages,
        )
        return response

    def parse_regions_response(self, regions_response: dict) -> YouTubeListResponse:
        regions: list[Region] = [
            Region(
                id=region['id'],
                snippet=RegionSnippet(
                    gl=region['snippet']['gl'], name=region['snippet']['name']
                ),
            )
            for region in regions_response['items']
        ]
        response: YouTubeListResponse = YouTubeListResponse(
            kind=regions_response['kind'],
            etag=regions_response['etag'],
            items=regions,
        )
        return response

    def parse_item(self, item: dict) -> Video:
        id_data: dict = self.parse_id(item)
        snippet_data: dict = self.parse_snippet(item['snippet'])
        statistics_data: dict = self.parse_statistics(item['statistics'])
        content_details: dict = self.parse_content_details(item['contentDetails'])
        id_data.update(snippet_data)
        id_data.update(statistics_data)
        id_data.update(content_details)
        return Video(**id_data)

    def create_upload_request_dict(self, request: UploadVideo) -> dict:
        request_dict: dict = dict()
        if request.snippet:
            request_dict['snippet'] = dict()
            for key, value in request.snippet.model_dump().items():
                if value:
                    request_dict['snippet'][key] = value
        if request.localizations:
            request_dict['localizations'] = dict()
            for key, value in request.localizations.model_dump().items():
                if value:
                    request_dict['localizations'][key] = value
        if request.status:
            request_dict['status'] = dict()
            for key, value in request.status.model_dump().items():
                if value:
                    request_dict['status'][key] = value
        if request.recordingDetails:
            request_dict['recordingDetails'] = dict()
            for key, value in request.recordingDetails.model_dump().items():
                if value:
                    request_dict['recordingDetails'][key] = value
        part: str = ''
        body: dict = defaultdict(dict)
        if request_dict.get('snippet'):
            part += 'snippet'
            body['snippet'] = request_dict['snippet']
        if request_dict.get('localizations'):
            part += ',localizations'
            body['localizations'] = request_dict['localizations']
        if request_dict.get('status'):
            part += ',status'
            body['status'] = request_dict['status']
        if request_dict.get('contentDetails'):
            part += ',contentDetails'
            body['contentDetails'] = request_dict['contentDetails']
        return part, request_dict

    def find_video_by_id(self, video_id: str) -> YouTubeListResponse:
        request_filter: VideoFilter = VideoFilter(id=[video_id])
        part: VideoPart = VideoPart()
        optional_params: VideoOptionalParameters = VideoOptionalParameters()
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part, filter=request_filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(request_schema)
        find_video_request: dict = self.youtube_client.videos().list(**request_dict)
        find_video_result: dict[str, Any] = find_video_request.execute()
        return self.parse_youtube_list_response(find_video_result)

    def find_videos_by_ids(self, video_ids: list[str]) -> YouTubeListResponse:
        filter: VideoFilter = VideoFilter(id=video_ids)
        part: VideoPart = VideoPart()
        optional_params: VideoOptionalParameters = VideoOptionalParameters()
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part, filter=filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(request_schema)
        find_video_request: dict = self.youtube_client.videos().list(**request_dict)
        find_video_result: dict[str, int | str] = find_video_request.execute()
        return self.parse_youtube_list_response(find_video_result)

    def find_most_popular_video_by_region(
        self, region_code: str = 'US', category_id: str = ''
    ) -> list[Video]:
        request_filter: VideoFilter = VideoFilter(chart='mostPopular')
        part: VideoPart = VideoPart()
        optional_params: VideoOptionalParameters = VideoOptionalParameters(
            regionCode=region_code, videoCategoryId=category_id
        )
        request_schema: YouTubeRequest = YouTubeRequest(
            part=part, filter=request_filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(request_schema)
        find_video_request: dict = self.youtube_client.videos().list(**request_dict)
        find_video_result: dict[str, Any] = find_video_request.execute()
        return self.parse_youtube_list_response(find_video_result)

    def get_video_ratings(self, video_ids: list[str]) -> YouTubeListResponse:
        video_ids: str = ','.join(video_ids)
        find_video_rating_request: dict = self.youtube_client.videos().getRating(
            id=video_ids
        )
        find_video_rating_result: dict[
            str, int | str
        ] = find_video_rating_request.execute()
        return self.parse_user_video_rating(find_video_rating_result)

    def rate_video(self, video_id: str, rating: str) -> None:
        """Add a like or dislike rating to a video or remove a rating from a video."""
        rating_request = self.youtube_client.videos().rate(id=video_id, rating=rating)
        rating_request.execute()

    def get_video_categories(self, region_code: str = 'us') -> YouTubeListResponse:
        categories_request = self.youtube_client.videoCategories().list(
            part='snippet', regionCode=region_code
        )
        categories_response = categories_request.execute()
        return self.parse_video_categories(categories_response)

    def upload_video(self, upload_req: UploadVideo) -> Video:
        part, body = self.create_upload_request_dict(upload_req)
        request = self.youtube_client.videos().insert(
            part=part, body=body, media_body=MediaFileUpload(upload_req.file)
        )
        response = request.execute()
        return response

    def update_video(self, upload_req: UploadVideo) -> Video:
        """Updates a video's metadata."""
        part, body = self.create_upload_request_dict(upload_req)
        video_update_request = self.youtube_client.videos().update(
            part=part, body=body, media_body=MediaFileUpload(upload_req.file)
        )
        video_update_response = video_update_request.execute()
        return video_update_response

    def delete_video(self, video_id: str) -> None:
        """Deletes a YouTube video."""
        video_delete_request = self.youtube_client.videos().delete(id=video_id)
        video_delete_request.execute()

    def set_video_thumbnail(self, video_id: str, thumbnail: str) -> YouTubeListResponse:
        set_thumbnail_request = self.youtube_client.thumbnails().set(
            videoId=video_id, media_body=MediaFileUpload(thumbnail)
        )
        set_thumbnail_response = set_thumbnail_request.execute()
        return set_thumbnail_response

    def list_video_abuse_report_reasons(self) -> YouTubeListResponse:
        video_abuse_request = self.youtube_client.videoAbuseReportReasons().list(
            part='snippet'
        )
        video_abuse_response = video_abuse_request.execute()
        return self.parse_video_abuse_report_reasons(video_abuse_response)

    def list_languages(self, language: str = 'en_US') -> YouTubeListResponse:
        list_language_request = self.youtube_client.i18nLanguages().list(
            part='snippet', hl=language
        )
        list_language_response = list_language_request.execute()
        return self.parse_languages_response(list_language_response)

    def list_regions(self, language: str = 'en_US') -> YouTubeListResponse:
        list_language_request = self.youtube_client.i18nRegions().list(
            part='snippet', hl=language
        )
        list_language_response = list_language_request.execute()
        return self.parse_regions_response(list_language_response)

    def report_video_abuse(self, abuse_report: VideoReportReasonSchema) -> None:
        report_abuse_request = self.youtube_client.videos().reportAbuse(
            body={**abuse_report.model_dump()}
        )
        report_abuse_request.execute()
