import shutil
from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException, UploadFile


def upload_photo(file: UploadFile, id: int, dir_name: str) -> None:
    upload_dir = Path.cwd() / 'uploads' / dir_name
    upload_dir.mkdir(parents=True, exist_ok=True)

    extensao = Path(file.filename).suffix
    nome_arquivo = f'{id}{extensao}'
    file_path = upload_dir / nome_arquivo

    existing_file = next(upload_dir.glob(f'{id}.*'), None)
    if existing_file:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=(
                f'Conflicting file detected for ID {id}: {existing_file.name}'
            ),
        )

    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
