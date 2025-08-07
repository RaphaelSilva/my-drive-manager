
from src.feature.backup_files_from.infrastructure.drivers.mediainfo.adapter import MediaInfoAdapter
from src.feature.backup_files_from.infrastructure.layers.media.abstract import AbstractMediaInfoLayer


class MediaInfoLayer:

    @staticmethod
    def create() -> AbstractMediaInfoLayer:
        return MediaInfoAdapter()
