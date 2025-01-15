import shutil
from pathlib import Path

import glob

from fastapi import UploadFile


def upload_photo(file: UploadFile, id: int, dir_name: str) -> None:
    upload_dir = Path.cwd() / 'uploads' / dir_name
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    photo_path = f'{upload_dir}/{id}.*'
    files = glob.glob(photo_path)
    if files:
        Path(files[0]).unlink()

    extension = Path(file.filename).suffix
    file_destiny = upload_dir / Path(f'{id}{extension}')
    with file_destiny.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return None
