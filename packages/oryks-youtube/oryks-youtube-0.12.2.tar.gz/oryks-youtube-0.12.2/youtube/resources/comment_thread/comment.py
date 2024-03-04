from typing import Any

from ...models import Comment, CommentSnippet
from ..resource import YouTubeResource


class CommentResource(YouTubeResource):
    def __init__(self, youtube_client: Any) -> None:
        super().__init__(youtube_client)

    def parse_author(self, comment_snippet: dict) -> dict:
        author: dict = dict()
        author['display_name'] = comment_snippet['authorDisplayName']
        author['profile_image_url'] = comment_snippet['authorProfileImageUrl']
        author['channel_url'] = comment_snippet['authorChannelUrl']
        author['channel_id'] = comment_snippet['authorChannelId']['value']
        return author

    def parse_snippet(self, snippet: dict) -> CommentSnippet:
        """Parse comment snippet"""
        parsed_snippet: dict[str, Any] = dict()
        parsed_snippet['channel_id'] = snippet['channelId']
        parsed_snippet['text_original'] = snippet['textOriginal']
        parsed_snippet['text_display'] = snippet['textDisplay']
        parsed_snippet['author'] = self.parse_author(snippet)
        parsed_snippet['can_rate'] = snippet['canRate']
        parsed_snippet['viewer_rating'] = snippet['viewerRating']
        parsed_snippet['like_count'] = snippet['likeCount']
        parsed_snippet['updated_at'] = snippet['updatedAt']
        parsed_snippet['published_at'] = snippet['publishedAt']
        parsed_snippet['parent_id'] = snippet.get('parentId', None)
        return CommentSnippet(**parsed_snippet)

    def parse_item(self, item: dict) -> Comment:
        id_data: dict = self.parse_id(item)
        snippet_data: dict = dict(snippet=self.parse_snippet(item['snippet']))
        id_data.update(snippet_data)
        return Comment(**id_data)
