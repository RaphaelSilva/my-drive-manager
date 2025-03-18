
from src.feature.backup_photos_from.domain.repositories.media_manager import MediaManagerRepository
from src.feature.backup_photos_from.domain.repositories.queue import QueueRepository
from src.shared.domain.business.abstraction import Business


class MediaQueuePreparer(Business):
    def __init__(self,
                 folder_source: str,
                 folder_destination: str,
                 midia_repository: MediaManagerRepository,
                 queue_repository: QueueRepository):
        self.path_source = folder_source
        self.path_destination = folder_destination
        self.file_system = midia_repository
        self.queue = queue_repository

    def execute(self) -> None:
        for file in self.file_system.list_all_midias_from_folder(self.path_source):
            self.queue.put({
                'file': file.to_json(),
                'source': self.path_source,
                'destination': self.path_destination
            })
            
