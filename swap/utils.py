from .git import git_clone, git_pull
from os import path
import tempfile


def get_work_dir(remote):
    folder = remote.split('/')[-1].split('.')[0]
    return path.join(tempfile.gettempdir(), folder)


def get_remote_path(remote_url):
    work_dir = get_work_dir(remote_url)

    if not path.exists(work_dir):
        git_clone(remote_url, work_dir)
    else:
        git_pull(work_dir)

    return work_dir

def split_path(string):
    out_path, in_path = string.split(':')
    if '@' in in_path:
        in_path, commit_id = in_path.split('@')
    else:
        commit_id = None
    return out_path, in_path, commit_id


def check_path(item):
    if path.isfile(item):
        return True
    elif path.isdir(item):
        return True
    exit('You must choose a file or a directory')
