import glob
from pathlib import Path


def file_path(id: int, dir_name: str) -> str:
    """
    Generates the file path to where it's been served for
    a given ID and directory name.

    Args:
        id (int): The ID of the file.
        dir_name (str): The name of the directory where the file is located.

    Returns:
        str: The URL path to the file or an empty string if no file
        is found
    """
    photo_path = Path.cwd() / 'uploads' / dir_name
    photo_path = f'{photo_path}/{id}.*'

    files = glob.glob(photo_path)
    if files:
        file_name = Path(files[0]).name
        return dir_name + '/' + file_name
    else:
        return ''
