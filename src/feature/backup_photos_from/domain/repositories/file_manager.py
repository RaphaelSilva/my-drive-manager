class FileManagerRepository:

    def __init__(self, file_manager_layer: AbstractFileManagerLayer):
        self.file_manager = file_manager_layer

    def get_files_in_folder(self, path: str) -> list[str]:
        super().__init__()




