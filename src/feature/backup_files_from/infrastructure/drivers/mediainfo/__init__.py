from src.feature.backup_files_from.infrastructure.layers.media.abstract import MediaInfoError
from src.feature.backup_files_from.infrastructure.layers.media.concrete import MediaInfoLayer


async def test_mediainfo(args):
    mediainfo = MediaInfoLayer.create()
    midia_date = mediainfo.extractDate(
        "target/bk/b8defba0-b518-4b38-98e0-29f7585272b4.mp4")
    print(f"Midia date: {midia_date}")
    midia_date = mediainfo.extractDate(
        "target/bk/b8defba0-b518-4b38-98e0-29f7585272b4 copy.mp4")
    print(f"Midia date: {midia_date}")
    try:
        midia_date = mediainfo.extractDate("target/bk/no_existe_file.mp4")
    except MediaInfoError as e:
        print(f"Error extracting media date: {e}")
