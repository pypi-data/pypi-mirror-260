from enum import Enum


class Scopes(Enum):
    youtube_force_ssl = 'https://www.googleapis.com/auth/youtube.force-ssl'
    youtube_readonly = 'https://www.googleapis.com/auth/youtube.readonly'
    youtube_upload = 'https://www.googleapis.com/auth/youtube.upload'
    youtube = 'https://www.googleapis.com/auth/youtube'
    youtubepartner = 'https://www.googleapis.com/auth/youtubepartner'
