# Adapter for MediaInfo to extract media file information.
# This adapter uses the pymediainfo library to parse media files and extract their creation date.
# External dependencies:
# - pymediainfo: A Python wrapper for the MediaInfo library.
#     How to install:
#     pip install pymediainfo
#     How to install on macOS:
#     brew install mediainfo
#     How to install on Linux:
#     sudo apt-get install mediainfo
#     How to install on Windows:
#     Download the MediaInfo installer from https://mediaarea.net/en/MediaInfo/Download/
#     and follow the installation instructions.

from abc import abstractmethod
from datetime import datetime
from pymediainfo import MediaInfo
from src.feature.backup_files_from.infrastructure.layers.media.abstract import AbstractMediaInfoLayer, MediaInfoError


def convert_to_datetime(date_str: str) -> datetime:
    # Assuming the date string is in the format 'YYYY-MM-DD HH:MM:SS UTC'
    # The string might start with 'UTC ', so we remove it if present.
    if date_str.startswith("UTC "):
        date_str = date_str[4:]
    # The string might end with ' UTC', so we remove it if present.
    if date_str.endswith(" UTC"):
        date_str = date_str[:-4]
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


class MediaInfoAdapter(AbstractMediaInfoLayer):
    def __init__(self, path: str = ""):
        self.path = path

    def extractDate(self) -> datetime:
        try:
            media_info = MediaInfo.parse(self.path)
            for track in media_info.tracks:
                if track.track_type == "General":
                    date_str = track.file_creation_date
                    return convert_to_datetime(date_str)
            raise MediaInfoError(
                f"No creation date found in media file: {self.path}")
        except Exception as e:
            raise MediaInfoError(
                f"Error extracting date from media file: {self.path}. Error: {e}"
            ) from e

    def resumeInfoGeneral(self, media_info=None) -> dict:
        media_info = media_info or MediaInfo.parse(self.path)
        info = {}
        for track in media_info.tracks:
            if track.track_type == "General":
                info["duration"] = track.duration
                info["file_size"] = track.file_size
                info["format"] = track.format
                info["bit_rate"] = track.bit_rate
                info["file_creation_date"] = track.file_creation_date
                info["file_creation_date__local"] = track.file_creation_date__local
                info["file_last_modification_date"] = track.file_last_modification_date
                info["file_last_modification_date__local"] = track.file_last_modification_date__local
        return info

    @abstractmethod
    def resumeInfo(self) -> dict:
        raise NotImplementedError(
            "This method should be implemented in subclasses.")


class MediaInfoForVideoAdapter(MediaInfoAdapter):
    def resumeInfo(self) -> dict:
        try:
            info = super().resumeInfoGeneral()
            return info
        except Exception as e:
            raise MediaInfoError(
                f"Error extracting info from media file: {self.path}. Error: {e}"
            ) from e


class MediaInfoForImageAdapter(MediaInfoAdapter):
    def resumeInfo(self) -> dict:
        try:
            media_info = MediaInfo.parse(self.path)
            info = super().resumeInfoGeneral(media_info)
            for track in media_info.tracks:
                if track.track_type == "Image":
                    info["width"] = track.width
                    info["height"] = track.height
                    info["compression_mode"] = track.compression_mode
                    info["format_extensions_usually_used"] = track.format_extensions_usually_used
            return info
        except Exception as e:
            raise MediaInfoError(
                f"Error extracting info from media file: {self.path}. Error: {e}"
            ) from e
