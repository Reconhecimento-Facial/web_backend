import shutil
from pathlib import Path

from fastapi import UploadFile


def upload_photo(file: UploadFile, id: int, dir_name: str) -> None:
    upload_dir = Path.cwd() / 'uploads' / dir_name
    upload_dir.mkdir(parents=True, exist_ok=True)

    extensao = Path(file.filename).suffix
    nome_arquivo = f'{id}{extensao}'
    file_path = upload_dir / nome_arquivo

    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
