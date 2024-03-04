from typing import Any

import googleapiclient.errors

from youtube.models import Resource

from ...exceptions import SubscriptionDuplicate, SubscriptionForbidden, SubscriptionNotFound
from ...models import BaseContentDetails, BaseSnippet, Subscription, SubscriptionSnippet
from ...schemas import (
    SubscriptionFilter,
    SubscriptionOptionalParameters,
    SubscriptionPart,
    YouTubeRequest,
    YouTubeResponse,
)
from ..resource import YouTubeResource


class YouTubeSubscription(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)

    def parse_snippet(self, snippet_data: dict[str, Any]) -> SubscriptionSnippet:
        base_snippet: BaseSnippet = self.parse_base_snippet(snippet_data)

    def parse_item(self, item: dict) -> Resource:
        return super().parse_item(item)

    def list_channel_subscriptions(self, request: YouTubeRequest) -> YouTubeResponse:
        request_dict = self.create_request_dict(request)
        actvities_request = self.youtube_client.subscriptions().list(**request_dict)
        actvities_response = actvities_request.execute()
        return actvities_response

    def list_my_subscriptions(self) -> YouTubeResponse:
        filter: SubscriptionFilter = SubscriptionFilter(mine=True)
        part: SubscriptionPart = SubscriptionPart()
        optional_params: SubscriptionOptionalParameters = (
            SubscriptionOptionalParameters()
        )
        youtube_request: YouTubeRequest = YouTubeRequest(
            part=part, filter=filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(youtube_request)
        subscriptions_request = self.youtube_client.subscriptions().list(**request_dict)
        subscriptions_response = subscriptions_request.execute()
        return subscriptions_response

    def do_i_subscribe(self, channel_id: str) -> bool:
        filter: SubscriptionFilter = SubscriptionFilter(mine=True)
        part: SubscriptionPart = SubscriptionPart()
        optional_params: SubscriptionOptionalParameters = (
            SubscriptionOptionalParameters()
        )
        youtube_request: YouTubeRequest = YouTubeRequest(
            part=part, filter=filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(youtube_request)
        actvities_request = self.youtube_client.subscriptions().list(**request_dict)
        actvities_response = actvities_request.execute()
        return actvities_response

    def is_subscribed(self, channel_id: str, user_channel: str) -> bool:
        filter: SubscriptionFilter = SubscriptionFilter(channelId=user_channel)
        part: SubscriptionPart = SubscriptionPart()
        optional_params: SubscriptionOptionalParameters = (
            SubscriptionOptionalParameters(forChannelId=channel_id)
        )
        youtube_request: YouTubeRequest = YouTubeRequest(
            part=part, filter=filter, optional_parameters=optional_params
        )
        request_dict = self.create_request_dict(youtube_request)
        actvities_request = self.youtube_client.subscriptions().list(**request_dict)
        actvities_response = actvities_request.execute()
        return actvities_response

    def subscribe_to_channel(self, channel_id: str) -> Subscription:
        try:
            subscription_request = self.youtube_client.subscriptions().insert(
                part=','.join(SubscriptionPart().part),
                body={
                    'snippet': {
                        'resourceId': {
                            'kind': 'youtube#channel',
                            'channelId': channel_id,
                        }
                    }
                },
            )
            subscription_response = subscription_request.execute()
        except googleapiclient.errors.HttpError as e:
            error_str: str = e.error_details[0]['reason']
            if error_str == 'subscriptionDuplicate':
                raise SubscriptionDuplicate('That subscription already exists!')
        return subscription_response

    def unsubscribe_from_channel(self, subscription_id: str) -> None:
        try:
            unsubscribe_request = self.youtube_client.subscriptions().delete(
                id=subscription_id
            )
            unsubscribe_request.execute()
        except googleapiclient.errors.HttpError as e:
            error_str: str = e.error_details[0]['reason']
            if error_str == 'subscriptionNotFound':
                raise SubscriptionNotFound('That subscription was not found.')
