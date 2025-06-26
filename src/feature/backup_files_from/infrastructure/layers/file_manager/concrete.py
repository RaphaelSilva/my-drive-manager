
import platform

from src.feature.backup_files_from.infrastructure.drivers.systems.linux.adapter import \
    LinuxDriverManeger
from src.feature.backup_files_from.infrastructure.drivers.systems.mac.adapter import \
    MacDriverManeger
from src.feature.backup_files_from.infrastructure.drivers.systems.windows.adapter import \
    WindowsDriverManeger


class MediaManagerLayer:
    def __init__(self, media_manager):
        self.media_manager = media_manager

    @staticmethod
    def create():
        system = platform.system().lower()
        if system == 'windows':
            return WindowsDriverManeger()
        elif system == 'linux':
            return LinuxDriverManeger()
        elif system == 'darwin':  # macOS
            return MacDriverManeger()
        else:
            raise NotImplementedError(
                f"Unsupported operating system: {system}")
