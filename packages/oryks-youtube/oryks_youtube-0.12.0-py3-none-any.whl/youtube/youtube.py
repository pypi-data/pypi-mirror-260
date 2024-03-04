from collections.abc import Iterator
from typing import Any, Optional

from oryks_google_oauth import GoogleOAuth, YouTubeScopes
from pydantic import BaseModel

from .models import (
    Caption,
    ChannelSection,
    Comment,
    CommentThread,
    Playlist,
    PlaylistItem,
    Subscription,
    Video,
)
from .resources.channel import YouTubeChannel
from .resources.comment_thread import YouTubeCommentThread
from .resources.playlist import YouTubePlaylist
from .resources.playlist_item import YouTubePlaylistItem
from .resources.search import YouTubeSearch
from .resources.subscription import YouTubeSubscription
from .resources.video import YouTubeVideo
from .resources.activity import YouTubeActivity
from .schemas import (
    CreatePlaylist,
    CreatePlaylistItem,
    InsertChannelSection,
    ThumbnailSetResponse,
    UploadVideo,
    VideoReportReasonSchema,
    YouTubeListResponse,
    YouTubeRequest,
    YouTubeResponse,
)


class YouTube(BaseModel):
    """Provides methods for interacting with the YouTube API.

    This class acts as an interface to the YouTube API, providing methods for interacting with
    the YouTube V3 API.

    Attributes
    ----------
    client_secret_file: str
        The path to the json file containing your authentication information.
    """

    client_secret_file: Optional[str] = None
    authenticated: Optional[bool] = False
    youtube_client: Optional[Any] = None

    def authenticate(self, client_secret_file: Optional[str] = None) -> None:
        """Authenticate the requests made to youtube.

        Used to generate the credentials that are used when authenticating requests to youtube.

        Parameters
        ----------
        client_secret_file: str
            The path to clients secret json file from Google

        Raises
        ------
        ValueError:
            When the client secrets file is not provided
        FileNotFoundError:
            When the secrets file path is not found
        """
        if client_secret_file:
            self.client_secret_file = client_secret_file
        if not self.client_secret_file:
            raise ValueError('The client secret file must be provided.')
        api_service_name: str = 'youtube'
        api_version: str = 'v3'
        credentials_dir: str = '.youtube'
        scopes: list[str] = [
            YouTubeScopes.youtube.value,
            YouTubeScopes.youtube_force_ssl.value,
            YouTubeScopes.youtube_upload.value,
        ]
        oauth: GoogleOAuth = GoogleOAuth(
            secrets_file=self.client_secret_file,
            scopes=scopes,
            api_service_name=api_service_name,
            api_version=api_version,
            credentials_dir=credentials_dir,
        )
        youtube_client = oauth.authenticate_google_server()
        return youtube_client

    def search(self, search_schema: YouTubeRequest) -> YouTubeResponse:
        """Used to search through youtube for videos, playlists and channels.

        Parameters
        ----------
        search_schema: YouTubeRequest
            An instance of YouTubeRequest that contains all the details needed to search.
        Returns
        -------
        YouTubeResponse:
            An instance of YouTubeResponse that has al the search results.
        """
        search: YouTubeSearch = YouTubeSearch(youtube_client=self.youtube_client)
        search_results: YouTubeResponse = search.search(search_schema)
        return search_results

    def get_search_iterator(self, search_schema: YouTubeRequest) -> Iterator:
        """Return an iterator that can be used to iterate over search results.

        Parameters
        ----------
        search_schema: YouTubeRequest
            An instance of YouTubeRequest that contains all the details needed to search.
        Returns
        -------
        Iterator:
            An iterator that can be used to iterate over the search results.
        """
        search: YouTubeSearch = YouTubeSearch(youtube_client=self.youtube_client)
        return search.get_search_iterator(search_schema)

    def find_channel_by_name(self, display_name: str) -> YouTubeResponse:
        """Find a channel's details when given the channel title.

        Parameters
        ----------
        display_name: str
            The name of the youtube channel.
        Returns
        -------
        YouTubeResponse:
            A youtube response consisting of channels whose names match the provided names
        """
        search: YouTubeSearch = YouTubeSearch(youtube_client=self.youtube_client)
        return search.find_channel_by_name(display_name)

    def get_video_ratings(self, video_ids: list[str]) -> YouTubeListResponse:
        """Find out whether or not you liked the videos whose ids are provided.

        You provide it with a list of video ids and for each video it will tell you whether
        or not you have liked that video.

        Parameters
        ----------
        video_ids: list[str]:
            A list of strings of video ids
        Returns
        -------
        list[str]:
            A list of strings showing whether or not you liked a given video.
        """
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.get_video_ratings(video_ids)

    def find_video_by_id(self, video_id: str) -> YouTubeListResponse:
        """Find a single video by providing the video's id.

        Parameters
        ----------
        video_id: str
            The video's id
        Returns
        -------
        Video:
            A Video instance
        """
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.find_video_by_id(video_id)

    def find_videos_by_ids(self, video_ids: list[str]) -> YouTubeListResponse:
        """Find a many videos by providing a list of video ids.

        Parameters
        ----------
        video_ids: list[str]
            A list of video ids
        Returns
        -------
        list[Video]:
            A list of Video instances
        """
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.find_videos_by_ids(video_ids)

    def find_most_popular_video_by_region(
        self, region_code: str = 'US', category_id: str = ''
    ) -> list[Video]:
        """Get the most popular videos in a given region and category.

        Parameters
        ----------
        region_code: str
            A string representing the region code.
        category_id: str
            The category to find. This is a string number i.e '22'
        Returns
        -------
        list[Video]:
            A list of the most popular videos
        """
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.find_most_popular_video_by_region(region_code, category_id)

    def report_video_abuse(self, abuse_report: VideoReportReasonSchema) -> None:
        """Report a video that you deem as harmful or infringing on copyrights.

        Parameters
        ----------
        abuse_report: VideoReportAbuse
            An instance of VideoReportAbuse with all the details needed to report.
        """
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.report_video_abuse(abuse_report)

    def update_video(self, update_req: UploadVideo) -> Video:
        """Updates a video's metadata."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.update_video(update_req)

    def delete_video(self, video_id: str) -> None:
        """Deletes a YouTube video."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.delete_video(video_id)

    def upload_video(self, upload_req: UploadVideo) -> Video:
        """Upload a YouTube video."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.upload_video(upload_req)

    def rate_video(self, video_id: str, rating: str) -> None:
        """Add a like or dislike rating to a video or remove a rating from a video."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        video.rate_video(video_id, rating)

    def find_channel_by_id(self, channel_id: str) -> YouTubeListResponse:
        """Find a youtube channel given its id."""
        channel: YouTubeChannel = YouTubeChannel(youtube_client=self.youtube_client)
        return channel.find_channel_by_id(channel_id)

    def find_channels_by_ids(self, channel_ids: list[str]) -> YouTubeListResponse:
        """Find many channels given their ids."""
        channel: YouTubeChannel = YouTubeChannel(youtube_client=self.youtube_client)
        return channel.find_channels_by_ids(channel_ids)

    def find_my_channel(self) -> YouTubeListResponse:
        """Find the details fo your youtube channel."""
        channel: YouTubeChannel = YouTubeChannel(youtube_client=self.youtube_client)
        return channel.find_my_channel()

    def find_channel_playlists(
        self, channel_id: str, max_results: int = 25
    ) -> YouTubeListResponse:
        """Find the playlists for a given channel."""
        playlist: YouTubePlaylist = YouTubePlaylist(youtube_client=self.youtube_client)
        return playlist.find_channel_playlists(channel_id, max_results)

    def find_my_playlists(self) -> YouTubeListResponse:
        """Find the playlists in your channel."""
        playlist: YouTubePlaylist = YouTubePlaylist(youtube_client=self.youtube_client)
        return playlist.find_my_playlists()

    def get_my_playlists_iterator(self, max_results: int = 10) -> Iterator:
        """Get an iterator for iterating through playlists in your channel."""
        playlist: YouTubePlaylist = YouTubePlaylist(youtube_client=self.youtube_client)
        return playlist.get_my_playlists_iterator(max_results)

    def insert_playlist(self, playlist_schema: CreatePlaylist) -> Playlist:
        """Create a new playlist in your channel."""
        playlist: YouTubePlaylist = YouTubePlaylist(youtube_client=self.youtube_client)
        return playlist.insert_playlist(playlist_schema)

    def update_playlist(
        self, playlist_id: str, playlist_schema: CreatePlaylist
    ) -> Playlist:
        """Update a playlist in your channel."""
        playlist: YouTubePlaylist = YouTubePlaylist(youtube_client=self.youtube_client)
        return playlist.update_playlist(playlist_id, playlist_schema)

    def delete_playlist(self, playlist_id: str) -> None:
        """Delete a playlist in your channel."""
        playlist: YouTubePlaylist = YouTubePlaylist(youtube_client=self.youtube_client)
        return playlist.delete_playlist(playlist_id)

    def find_playlist_items(
        self, playlist_id: str, max_results: Optional[int] = 25
    ) -> YouTubeResponse:
        """Find a particular video in your playlist."""
        playlist_item: YouTubePlaylistItem = YouTubePlaylistItem(
            youtube_client=self.youtube_client
        )
        return playlist_item.find_playlist_items(playlist_id, max_results)

    def find_playlist_items_by_ids(
        self, playlist_item_ids: list[str]
    ) -> YouTubeListResponse:
        """Find various playlist videos given their ids."""
        playlist_item: YouTubePlaylistItem = YouTubePlaylistItem(
            youtube_client=self.youtube_client
        )
        return playlist_item.find_playlist_items_by_ids(playlist_item_ids)

    def insert_playlist_item(self, create_item: CreatePlaylistItem) -> PlaylistItem:
        """Add a video to a playlist."""
        playlist_item: YouTubePlaylistItem = YouTubePlaylistItem(
            youtube_client=self.youtube_client
        )
        return playlist_item.insert_playlist_item(create_item)

    def update_playlist_item(
        self, playlist_id: str, playlist_item_id: str, video_id: str, position: int = 1
    ) -> PlaylistItem:
        """Update a given video details in a playlist."""
        playlist_item: YouTubePlaylistItem = YouTubePlaylistItem(
            youtube_client=self.youtube_client
        )
        return playlist_item.update_playlist_item(
            playlist_id, playlist_item_id, video_id, position
        )

    def delete_playlist_item(self, playlist_item_id: str) -> None:
        """Delete a video from a playlist."""
        playlist_item: YouTubePlaylistItem = YouTubePlaylistItem(
            youtube_client=self.youtube_client
        )
        return playlist_item.delete_playlist_item(playlist_item_id)

    def get_video_categories(
        self, region_code: Optional[str] = ''
    ) -> YouTubeListResponse:
        """List all the video categories on youtube."""
        youtube_video = YouTubeVideo(youtube_client=self.youtube_client)
        return youtube_video.get_video_categories(region_code=region_code)

    def find_video_comments(self, request: YouTubeRequest) -> YouTubeResponse:
        """Get a particular video's comments."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.find_video_comments(request)

    def get_comments_iterator(self, request_schema: YouTubeResponse) -> Iterator:
        """Get an iterator for going through a videos comments."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.get_comments_iterator(request_schema)

    def find_all_channel_comments(self, request: YouTubeRequest) -> YouTubeListResponse:
        """Get a particular channels's comments."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.find_all_channel_comments(request)

    def insert_comment(self, video_id: str, comment: str) -> CommentThread:
        """Comment on a given video."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.insert_comment(video_id, comment)

    def get_comment_replies(self, comment_id: str) -> list[Comment]:
        """Get the replies for a given comment."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.get_comment_replies(comment_id)

    def get_comment(self, comment_id: str) -> YouTubeListResponse:
        """Get a comments, given its id."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.get_comment(comment_id)

    def get_comments(self, comment_ids: list[str]) -> YouTubeListResponse:
        """Get various comments given their ids."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.get_comments(comment_ids)

    def reply_to_comment(self, comment_id: str, comment: str) -> Comment:
        """Reply to the given comment."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.reply_to_comment(comment_id, comment)

    def update_comment(self, comment_id: str, comment: str) -> Comment:
        """Update a comments."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.update_comment(comment_id, comment)

    def delete_comment(self, comment_id: str) -> None:
        """Delete a comment."""
        comment_thread: YouTubeCommentThread = YouTubeCommentThread(
            youtube_client=self.youtube_client
        )
        return comment_thread.delete_comment(comment_id)

    def list_channel_activities(self, request: YouTubeRequest) -> YouTubeResponse:
        """List all the activities of the given channel, such as uploads."""
        activity: YouTubeActivity = YouTubeActivity(youtube_client=self.youtube_client)
        return activity.list_channel_activity(request)

    def list_my_activities(self) -> YouTubeListResponse:
        """List all the activities for your channel, such as creating a playlist."""
        activity: YouTubeActivity = YouTubeActivity(youtube_client=self.youtube_client)
        return activity.list_my_activities()

    def list_video_captions(self, video_id: str) -> Caption:
        raise NotImplementedError()

    def insert_video_caption(self, video_id: str) -> None:
        raise NotImplementedError()

    def update_video_caption(self, caption_id: str) -> None:
        raise NotImplementedError()

    def download_video_caption(self, caption_id: str) -> None:
        raise NotImplementedError()

    def delete_video_caption(self, caption_id: str) -> None:
        raise NotImplementedError()

    def upload_channel_banner(self, media_file: str, channel_id: str) -> None:
        raise NotImplementedError()

    def list_channel_sections(self, channel_id: str) -> YouTubeListResponse:
        """List a channel's sections."""
        raise NotImplementedError()

    def list_my_channel_sections(self) -> YouTubeListResponse:
        """List your channel sections."""
        raise NotImplementedError()

    def insert_channel_section(self, request: InsertChannelSection) -> ChannelSection:
        """Insert a new channle section."""
        raise NotImplementedError()

    def update_channel_section(self, channel_section_id: str) -> None:
        """Update a channel section."""
        raise NotImplementedError()

    def delete_channel_section(self, channel_section_id: str) -> None:
        """Delete a channel section."""
        raise NotImplementedError()

    def list_languages(self, language: str = 'en_US') -> YouTubeListResponse:
        """List all the languages youtube supports."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.list_languages(language)

    def list_regions(self, language: str = 'en_US') -> YouTubeListResponse:
        """List all the regions youtube supports."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.list_regions(language)

    def set_watermark(self, channel_id: str) -> None:
        """Set a video's watermarks."""
        raise NotImplementedError()

    def unset_watermark(self, channel_id: str) -> None:
        """Remove a video's watermark."""
        raise NotImplementedError()

    def list_video_abuse_report_reasons(self) -> YouTubeListResponse:
        """List reasons that can be used to report a video."""
        video: YouTubeVideo = YouTubeVideo(youtube_client=self.youtube_client)
        return video.list_video_abuse_report_reasons()

    def set_video_thumbnail(
        self, video_id: str, thumbnail: str
    ) -> ThumbnailSetResponse:
        """Set a video's thumbnail."""
        raise NotImplementedError()

    def list_channel_subscriptions(self, request: YouTubeRequest) -> YouTubeResponse:
        """List the given channel's subscriptions."""
        subscription: YouTubeSubscription = YouTubeSubscription(
            youtube_client=self.youtube_client
        )
        return subscription.list_channel_subscriptions(request)

    def list_my_subscriptions(self) -> YouTubeResponse:
        """List the channels I subscribe to."""
        subscription: YouTubeSubscription = YouTubeSubscription(
            youtube_client=self.youtube_client
        )
        return subscription.list_my_subscriptions()

    def do_i_subscribe(self, channel_id: str) -> bool:
        """Check if I subscribe to the given channel."""
        subscription: YouTubeSubscription = YouTubeSubscription(
            youtube_client=self.youtube_client
        )
        return subscription.do_i_subscribe(channel_id)

    def is_subscribed(self, channel_id: str, user_channel: str) -> bool:
        """Check if one channel subscribes to another channel.

        Parameters
        ----------
        channel_id: str
            The channel id of the channel to which subscription is being confirmed.
        user_channel: str
            The channel id of the channel to check if its subscribed.
        Returns
        -------
        bool:
            Whether user_channel subscribes to channel_id
        """
        subscription: YouTubeSubscription = YouTubeSubscription(
            youtube_client=self.youtube_client
        )
        return subscription.is_subscribed(
            channel_id=channel_id, user_channel=user_channel
        )

    def subscribe_to_channel(self, channel_id: str) -> Subscription:
        """Subscribe to a youtube channel.

        Parameters
        ----------
        channel_id: str
            The id of the channel you want to subscribe to.
        Returns
        -------
        Subscription:
            An instance of subscription with all the details on the channel subscription.
        """
        subscription: YouTubeSubscription = YouTubeSubscription(
            youtube_client=self.youtube_client
        )
        return subscription.subscribe_to_channel(channel_id=channel_id)

    def unsubscribe_from_channel(self, subscription_id: str) -> None:
        """Unsubscribe from a youtube channel.

        Parameters
        ----------
        subscription_id: str
            The subscription id. You can get this by listing your subscriptions.
        """
        subscription: YouTubeSubscription = YouTubeSubscription(
            youtube_client=self.youtube_client
        )
        return subscription.unsubscribe_from_channel(subscription_id)

    def list_activities(self) -> dict:
        """List your activities on youtube including subscriptions, likes."""
        raise NotImplementedError()
