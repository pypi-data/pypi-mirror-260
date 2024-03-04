from .resource import Resource


class YouTubeVideoRating(Resource):
    video_id: str
    rating: str
