from os import path
import tempfile


def get_work_dir(remote):
    folder = remote.split('/')[-1].split('.')[0]
    return path.join(tempfile.gettempdir(), folder)
