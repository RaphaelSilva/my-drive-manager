
from src.feature.backup_files_from.domain.repositories.media_manager import MediaManagerRepository
from src.feature.backup_files_from.domain.repositories.queue import QueueRepository
from src.shared.domain.business.abstraction import Business


class QueuedMediaFileMover(Business):
    def __init__(self,
                 midia_repository: MediaManagerRepository,
                 queue_repository: QueueRepository):
        self.file_system = midia_repository
        self.queue = queue_repository

    def execute(self) -> None:
        try:
            message = self.queue.get()
            file = message.get('file')
            destination = message.get('destination')
            destination_folder = self.file_system.create_date_folder(destination)
            self.file_system.move_file(file, destination_folder)
        except Exception as error:
            self.queue.dlq(message, error)
            raise error
