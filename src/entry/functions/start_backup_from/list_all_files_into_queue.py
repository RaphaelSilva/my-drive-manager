
from src.feature.backup_files_from.domain.business.media_queue_preparer import MediaQueuePreparer
from src.feature.backup_files_from.domain.repositories.media_manager import MediaManagerRepository
from src.feature.backup_files_from.domain.repositories.queue import QueueRepository
from src.feature.backup_files_from.infrastructure.layers.file_manager.concrete import MediaManagerLayer
from src.feature.backup_files_from.infrastructure.layers.queue.concrete import QueueLayer


async def execute(origin, destination):    
    print(f"Listing all files from {origin} into queue for backup to {destination}")
    media_manager_repository = MediaManagerRepository(
        file_manager_layer=MediaManagerLayer.create()
    )
    queue_repository = QueueRepository(
        queue_layer=QueueLayer.create()
    )
    await MediaQueuePreparer(
        folder_source=origin,
        folder_destination=destination,
        midia_repository=media_manager_repository,
        queue_repository=queue_repository
    ).execute()
