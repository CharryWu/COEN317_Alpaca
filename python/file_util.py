import os
from log_util import log, bcolors

def get_path(root: str, relative_url: str):
    return os.path.join(os.path.abspath(root), relative_url.strip('/'))

def remove_files_by_suffix(url: str, type: str):
    log(f'{os.path.abspath(url)}, {type}', bcolors.WARNING)
    counter = 0
    for file in os.listdir(url):
        if file.endswith(type):
            os.remove(get_path(url, file))
            counter += 1
    log(f'{counter} {type} files removed in total', bcolors.WARNING)