
from src.feature.backup_files_from.domain.repositories.media_manager import MediaManagerRepository
from src.feature.backup_files_from.domain.repositories.queue import QueueRepository
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

    async def execute(self):
        for file in self.file_system.list_all_midias_from_folder(self.path_source):
            await self.queue.put(file)
