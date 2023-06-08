from os import listdir, remove
from os.path import join, abspath, isfile, exists
from pathlib import Path

import hashlib
import aiofiles
from log_util import log, bcolors
from fastapi import UploadFile

async def save_to_disk(file: UploadFile, dir: str, filename: str, chunksize: int = 8192):
    if not exists(dir):
        Path(dir).mkdir(parents=True)
    write_url = get_path(dir, filename)
    async with aiofiles.open(get_path(dir, filename), 'wb') as out_file:
        while content := await file.read(chunksize):  # async read chunk
            await out_file.write(content)  # async write chunk
        return write_url

def calculate_md5(file: UploadFile, chunksize: int = 8192):
    file_hash = hashlib.md5()
    while chunk := file.read(chunksize):
        file_hash.update(chunk)
    return file_hash.hexdigest()

def file_exists(file: UploadFile, dir: str):
    return isfile(join(dir, file.filename))

def get_path(root: str, relative_url: str):
    return join(abspath(root), relative_url.strip('/'))

def remove_files_by_suffix(url: str, type: str):
    log(f'{abspath(url)}, {type}', bcolors.WARNING)
    counter = 0
    for file in listdir(url):
        if file.endswith(type):
            remove(get_path(url, file))
            counter += 1
    log(f'{counter} {type} files removed in total', bcolors.WARNING)