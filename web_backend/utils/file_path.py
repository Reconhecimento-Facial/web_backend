import glob
from pathlib import Path


def file_path(id: int, dir_name: str) -> str:
    photo_path = Path.cwd() / 'uploads' / dir_name
    photo_path = f'{photo_path}/{id}.*'

    files = glob.glob(photo_path)
    file_name = ''
    if files:
        file_name = Path(files[0]).name

    return dir_name + '/' + file_name
