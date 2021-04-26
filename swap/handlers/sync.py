from argparse import Namespace
from termcolor import colored
from os import path

from swap.lock import check_lock, get_hash, update_lock
from swap.utils import get_work_dir, split_path
from swap.rsync import rsync
from swap.git import (
    git_current_branch,
    git_add_commit,
    git_new_branch,
    git_porcelain,
    git_clone,
    git_merge,
    git_pull,
    git_push,
)


def sync_component(options: Namespace, skip_checks=False, no_commit=False):
    if not skip_checks and git_porcelain('.'):
        exit('Please clean your working tree.')

    original_branch = git_current_branch('.')

    # TODO: Parallelism
    for git_url, modules in options.template.items():
        work_dir = get_work_dir(git_url)

        # If names are given check if names are prensent in this remote
        if options.NAME and not list(set(modules.keys()) & set(options.NAME)):
            continue

        # If path do not exist clone it from remote
        if not path.exists(work_dir):
            git_clone(git_url, work_dir)
        else:
            git_pull(work_dir)

        for name, p in modules.items():
            local_path, remote_path, commit_id = split_path(p)
            if commit_id:
                continue

            if not check_lock(options, name) and not options.force:
                if no_commit:
                    rsync(path.join(work_dir, remote_path), local_path, require_source=True)
                else:
                    source_branch = get_hash(options, name).get('local') or original_branch
                    branch = git_new_branch('.', source_branch)
                    rsync(path.join(work_dir, remote_path), local_path, require_source=True)
                    try:
                        git_add_commit('.', None)
                    except:
                        pass
                    if not git_merge('.', branch, original_branch):
                        print(colored(f'Merge of {name} failed!', 'red'))
                        print(colored('Fix merge conflicts then run `swp sync -f`', 'red'))
                        continue
            rsync(local_path, path.join(work_dir, remote_path))

        update_lock(options, git_url)

        try:
            git_add_commit(work_dir, options.commit_msg or None)
            git_push(work_dir)
        except:
            pass

    if not no_commit:
        try:
            git_add_commit('.', options.commit_msg or None)
        except:
            pass
