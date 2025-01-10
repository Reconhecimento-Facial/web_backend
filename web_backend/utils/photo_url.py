import glob
from pathlib import Path


def photo_url(id: int, dir_name: str) -> str:
    photo_path = Path.cwd() / 'uploads' / dir_name
    photo_path = f'{photo_path}/{id}.*'

    files = glob.glob(photo_path)
    if files:
        file_name = Path(files[0]).name
    else:
        file_name = ''

    return f'/{dir_name}/{file_name}'
