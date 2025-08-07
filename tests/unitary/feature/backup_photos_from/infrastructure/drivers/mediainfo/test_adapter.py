from datetime import datetime
from unittest.mock import patch, Mock

from pymediainfo import MediaInfo
from src.feature.backup_files_from.infrastructure.drivers.mediainfo.adapter import MediaInfoAdapter


@patch.object(MediaInfo, "parse", new_callable=Mock)
def test_send_message(mock_create_message):
    mock_create_message.return_value = Mock(
        tracks=[
            Mock(track_type="General", file_creation_date="2025-06-05 22:01:58 UTC"),
        ]
    )
    adapter = MediaInfoAdapter()
    date = adapter.extractDate("test.mp4")
    assert isinstance(date, datetime)
    assert date == datetime(2025, 6, 5, 22, 1, 58)
