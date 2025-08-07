from datetime import datetime
from pymediainfo import MediaInfo
from src.feature.backup_files_from.infrastructure.layers.media.abstract import AbstractMediaInfoLayer, MediaInfoError


class MediaInfoAdapter(AbstractMediaInfoLayer):

    def extractDate(self, path: str) -> datetime:
        try:
            media_info = MediaInfo.parse(path)
            for track in media_info.tracks:
                if track.track_type == "General":
                    return track.file_creation_date
            raise MediaInfoError(
                f"No creation date found in media file: {path}")
        except Exception as e:
            raise MediaInfoError(
                f"Error extracting date from media file: {path}. Error: {e}"
            ) from e
