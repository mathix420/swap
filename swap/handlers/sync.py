from argparse import Namespace
from termcolor import colored
from os import path

from swap.lock import check_lock, get_hash, update_lock
from swap.utils import get_remote_path, split_path
from swap.rsync import rsync
from swap.git import (
    git_current_branch,
    git_add_commit,
    git_new_branch,
    git_porcelain,
    git_checkout,
    git_merge,
    git_push,
)


def _in(a, b):
    return bool(list(set(a) & set(b)))


def _pull_merge(options, module_name, original_branch, remote, local):
    source_branch = get_hash(options, module_name).get(
        'local') or original_branch
    branch = git_new_branch('.', source_branch)

    rsync(remote, local, require_source=True)

    _commit('.', None)

    if not git_merge('.', branch, original_branch):
        print(colored(f'Merge of {module_name} failed!', 'red'))
        exit(colored('Fix merge conflicts then run `swp sync -f`', 'red'))

def _commit(path, msg):
    try:
        git_add_commit(path, msg)
    except:
        return False
    return True


def sync_remote(options, modules, work_dir, no_commit, default_branch):
    for module_name, p in modules.items():
        local_path, remote_folder, commit_id = split_path(p)
        remote_path = path.join(work_dir, remote_folder)
        remote_def_branch = git_current_branch(work_dir)

        if commit_id:
            git_checkout(work_dir, commit_id)

        need_to_pull = not check_lock(
            options, module_name) and not options.force

        # PULL remote changes to local
        if need_to_pull and no_commit:
            rsync(remote_path, local_path, require_source=True)
        elif need_to_pull:
            _pull_merge(options, module_name, default_branch, remote_path, local_path)
        elif not need_to_pull:
            print(f'{module_name} up to date!')

        if commit_id:
            git_checkout(work_dir, remote_def_branch)

        # PUSH local modifs to remote
        if not commit_id:
            rsync(local_path, remote_path)


def sync_component(options: Namespace, skip_checks=False, no_commit=False):
    if not skip_checks and git_porcelain('.'):
        exit('Please clean your working tree.')

    original_branch = git_current_branch('.')

    for git_url, modules in options.template.items():
        # If names are given check if names are prensent in this remote
        if options.NAME and not _in(modules.keys(), options.NAME):
            continue

        # If path do not exist clone it from remote
        work_dir = get_remote_path(git_url)

        sync_remote(options, modules, work_dir, no_commit, original_branch)

        # Update lock file
        update_lock(options, git_url)

        # If smth to commit, commit and push remote
        if _commit(work_dir, options.commit_msg or None):
            git_push(work_dir)

    if not no_commit:
        _commit('.', options.commit_msg or None)
