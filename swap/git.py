from datetime import datetime
import subprocess

OPTIONS = {
    'shell': True
}


def git_clone(remote, dest):
    subprocess.check_output(f'git clone {remote} {dest}', **OPTIONS)


def git_pull(dest):
    subprocess.check_output(f'git -C {dest} pull', **OPTIONS)


def git_checkout(dest, branch):
    subprocess.check_output(f'git -C {dest} checkout {branch}', **OPTIONS)


def git_porcelain(dest):
    e = subprocess.check_output(f'git -C {dest} status --porcelain', **OPTIONS)
    return bool(e)


def git_get_hash(dest):
    e = subprocess.check_output(f'git -C {dest} rev-parse HEAD', **OPTIONS)
    return e.decode('utf-8').strip()


def git_push(dest):
    subprocess.check_output(f'git -C {dest} push origin master', **OPTIONS)


def git_add_commit(dest, message=None):
    subprocess.check_output(f'git -C {dest} add --all', **OPTIONS)
    message = message or f'[UPDATE] {datetime.now()}'
    subprocess.check_output(f'git -C {dest} commit -m "{message}"', **OPTIONS)
