import subprocess

OPT = {
    'shell': True
}


def rsync(source_path, dest_path, exclude_file=None, exclude_paths=None, dry_run=False):
    command = 'rsync -ai --delete'

    if exclude_file:
        command += ' --exclude-from ' + exclude_file

    if exclude_paths:
        command += ''.join([f' --exclude {path}' for path in exclude_paths])

    if dry_run:
        command += ' --dry-run'

    e = subprocess.check_output(f'{command} {source_path} {dest_path}', **OPT)
    return bool(e)
