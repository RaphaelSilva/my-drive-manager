import json
from typing import Optional
from src.feature.backup_photos_from.domain.entities.file import FileDescription
from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import AbstractQueueLayer


class QueueRepository:
    def __init__(self, queue_layer: AbstractQueueLayer):
        self.queue = queue_layer

    async def put(self, file: FileDescription) -> None:
        json = file.to_json()
        await self.queue.send_message(json)

    async def get(self) -> Optional[FileDescription]:
        file_description = await self.queue.receive_message()
        return FileDescription.from_json(file_description) if file_description else None

    async def dlq(self, file: FileDescription, error: Exception) -> None:
        message = {
            "file": file.__dict__,
            "error": error.__dict__
        }
        message_json = json.dumps(message, indent=4)
        await self.queue.send_message_dlq(message_json)
