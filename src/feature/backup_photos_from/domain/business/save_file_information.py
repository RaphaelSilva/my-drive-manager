from src.shared.domain.business.abstraction import Business


class SaveFileInformation(Business):
    def __init__(self,
                 folder_source: str,
                 file_system_repository: FileSystemRepository,
                 queue_repository: QueueRepository):
        self.path = folder_source
        self.file_system = file_system_repository
        self.queue = queue_repository

    def execute(self) -> None:
        for file in self.file_system.get_files_in_folder(self.path):
            self.queue.put(file)
