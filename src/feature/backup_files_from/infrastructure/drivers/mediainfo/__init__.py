from src.feature.backup_files_from.infrastructure.layers.media.abstract import MediaInfoError
from src.feature.backup_files_from.infrastructure.layers.media.concrete import MediaInfoLayer


async def test_mediainfo(args):
    mediainfo = MediaInfoLayer.create(
        "target/bk/b8defba0-b518-4b38-98e0-29f7585272b4.mp4")
    midia_date = mediainfo.extractDate()
    print(f"Midia date: {midia_date}")
    mediainfo = MediaInfoLayer.create(
        "target/bk/b8defba0-b518-4b38-98e0-29f7585272b4 copy.mp4")
    midia_date = mediainfo.extractDate()
    print(f"Midia date: {midia_date}")
    try:
        mediainfo = MediaInfoLayer.create("target/bk/no_existe_file.mp4")
        midia_date = mediainfo.extractDate()
    except MediaInfoError as e:
        print(f"Error extracting media date: {e}")

    mediainfo = MediaInfoLayer.create(
        "target/bk/001064e2-3632-4b06-b132-7aa9c9cbf2ec.jpg")
    midia_date = mediainfo.extractDate()
    print(f"Midia date: {midia_date}")
