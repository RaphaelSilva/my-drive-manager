
from src.feature.backup_files_from.infrastructure.drivers.mediainfo.adapter import MediaInfoForImageAdapter, MediaInfoForVideoAdapter
from src.feature.backup_files_from.infrastructure.layers.media.abstract import AbstractMediaInfoLayer
import os

video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpg', '.mpeg', '.m4v'}

class MediaInfoLayer:

    @staticmethod
    def create(file_path: str) -> AbstractMediaInfoLayer:
        _, extension = os.path.splitext(file_path)
        if extension.lower() in video_extensions:
            return MediaInfoForVideoAdapter(file_path)
        return MediaInfoForImageAdapter(file_path)
