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

from datetime import datetime
from pymediainfo import MediaInfo
from src.feature.backup_files_from.infrastructure.layers.media.abstract import AbstractMediaInfoLayer, MediaInfoError


class MediaInfoAdapter(AbstractMediaInfoLayer):

    def extractDate(self, path: str) -> datetime:
        try:
            media_info = MediaInfo.parse(path)
            for track in media_info.tracks:
                if track.track_type == "General":
                    date_str = track.file_creation_date
                    # Assuming the date string is in the format 'YYYY-MM-DD HH:MM:SS UTC'
                    # The string might start with 'UTC ', so we remove it if present.
                    if date_str.startswith("UTC "):
                        date_str = date_str[4:]
                    # The string might end with ' UTC', so we remove it if present.
                    if date_str.endswith(" UTC"):
                        date_str = date_str[:-4]
                    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            raise MediaInfoError(
                f"No creation date found in media file: {path}")
        except Exception as e:
            raise MediaInfoError(
                f"Error extracting date from media file: {path}. Error: {e}"
            ) from e
