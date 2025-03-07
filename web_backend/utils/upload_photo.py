import glob
import shutil
from pathlib import Path

from fastapi import UploadFile

from web_backend.settings import Settings


def upload_photo(file: UploadFile, id: int, dir_name: str) -> None:
    upload_dir = Path(Settings().UPLOADS_DIR) / dir_name
    upload_dir.mkdir(parents=True, exist_ok=True)

    photo_path = f'{upload_dir}/{id}.*'
    files = glob.glob(photo_path)
    if files:
        Path(files[0]).unlink()

    extension = Path(file.filename).suffix
    file_destiny = upload_dir / Path(f'{id}{extension}')
    with file_destiny.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
