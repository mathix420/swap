from datetime import datetime
import subprocess

OPTIONS = {
    'shell': True
}


def git_clone(remote, dest):
    subprocess.check_output(f'git clone {remote} {dest}', **OPTIONS)


def git_pull(dest):
    subprocess.check_output(f'git -C {dest} pull', **OPTIONS)


def git_checkout(dest, branch, source=None):
    subprocess.check_output(f'git -C {dest} checkout {branch}', **OPTIONS)


def delete_branch(dest, branch):
    subprocess.check_output(f'git -C {dest} branch -d {branch}', **OPTIONS)


def git_merge(path, source, dest) -> bool:
    """
    Returns True if merge succeeded, False if conflicted.
    """

    git_checkout(path, dest)

    try:
        subprocess.check_output(
            f'LC_ALL=en_US git -C {path} merge {source}',
            **OPTIONS
        )
        delete_branch(path, source)
    except subprocess.CalledProcessError as error:                                                                                                   
        if 'CONFLICT' in error.output:
            delete_branch(path, source)
            return False
        raise error

    return True


def git_new_branch(dest, source) -> str:
    """
    Returns new branch name
    """

    ts = datetime.timestamp(datetime.utcnow())
    try:
        subprocess.check_output(
            f'git -C {dest} checkout -b swap/{ts} {source}',
            **OPTIONS
        )
    except subprocess.CalledProcessError:
        raise Exception('Cannot create a new branch!')
    return f'swap/{ts}'


def git_porcelain(dest):
    e = subprocess.check_output(f'git -C {dest} status --porcelain', **OPTIONS)
    return bool(e)


def git_current_branch(dest):
    e = subprocess.check_output(f'git -C {dest} branch --show-current', **OPTIONS)
    return e.decode('utf-8').strip()


def git_get_hash(dest) -> str:
    e = subprocess.check_output(f'git -C {dest} rev-parse HEAD', **OPTIONS)
    return e.decode('utf-8').strip()


def git_push(dest):
    subprocess.check_output(f'git -C {dest} push origin master', **OPTIONS)


def git_add_commit(dest, message=None):
    subprocess.check_output(f'git -C {dest} add --all', **OPTIONS)
    message = message or f'[SWAP] SYNC {datetime.utcnow()}'
    subprocess.check_output(f'git -C {dest} commit -m "{message}"', **OPTIONS)
