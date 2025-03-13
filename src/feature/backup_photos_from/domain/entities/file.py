class FileDescription:
    def __init__(self, file_name: str, file_path: str):
        self.file_name = file_name
        self.file_path = file_path

    def __str__(self):
        return f"FileDescription(file_name={self.file_name}, file_path={self.file_path})"

    def __repr__(self):
        return str(self)