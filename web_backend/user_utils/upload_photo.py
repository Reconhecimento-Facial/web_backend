from pathlib import Path
from fastapi import UploadFile
import shutil


def upload_photo(file: UploadFile, user_id: int) -> bool:

    upload_dir = Path.cwd() / 'uploads' / 'users_photos'
    upload_dir.mkdir(parents=True, exist_ok=True)

    extensao = Path(file.filename).suffix
    nome_arquivo = f'{user_id}{extensao}'
    file_path = upload_dir / nome_arquivo

    if file_path.exists():
        return False

    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return True