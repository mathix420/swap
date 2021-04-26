from os import path, remove
import subprocess
import shutil

OPT = {
    'shell': True
}


def rsync(source_path, dest_path, exclude_file=None, exclude_paths=None, dry_run=False, require_source=False):
    command = 'rsync -ai --delete'

    if require_source and not path.exists(source_path):
        return False
    elif not path.exists(source_path):
        if path.isdir(dest_path):
            shutil.rmtree(dest_path)
        else:
            remove(dest_path)
        return True

    if path.isdir(source_path):
        source_path = path.join(source_path, '')

    if exclude_file:
        command += ' --exclude-from ' + exclude_file

    if exclude_paths:
        command += ''.join([f' --exclude {p}' for p in exclude_paths])

    if dry_run:
        command += ' --dry-run'

    e = subprocess.check_output(f'{command} {source_path} {dest_path}', **OPT)
    return bool(e)
