import glob
from pathlib import Path


def photo_url(id: int, dir_name: str) -> str:
    photo_path = Path.cwd() / 'uploads' / dir_name
    photo_path = f'{photo_path}/{id}.*'

    files = glob.glob(photo_path)
    file_url = ''
    if files:
        file_url = '/' + dir_name + '/' + Path(files[0]).name

    return file_url
