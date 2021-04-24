from .utils import get_work_dir
from .git import git_get_hash

import json


global LOCKFILE_SAV
LOCKFILE_SAV = dict()


def load_lockfile(options) -> "dict[str, str]":
    if not globals()['LOCKFILE_SAV']:
        try:
            with open(options.l) as fp:
                globals()['LOCKFILE_SAV'] = json.load(fp)
        except IOError as e:
            if e.errno != 2:
                raise e
            globals()['LOCKFILE_SAV'] = {
                "0": 'Auto-generated file, do not edit nor delete!',
                "1": 'This file should be present in your version control system.'
            }

    return globals()['LOCKFILE_SAV']


def save_lockfile(options):
    with open(options.l, 'w') as fp:
        json.dump(globals()['LOCKFILE_SAV'], fp, indent=4, sort_keys=True)


def get_hash(options, name):
    return load_lockfile(options).get(name)


def update_lock(options, git_url: str) -> bool:
    has_changed = False
    load_lockfile(options)
    commit_hash = git_get_hash(get_work_dir(git_url))

    for component_name in options.template.get(git_url).keys():
        has_changed = has_changed or (
            globals()['LOCKFILE_SAV'].get(component_name) != commit_hash
        )
        globals()['LOCKFILE_SAV'][component_name] = commit_hash

    save_lockfile(options)
    return has_changed


def check_lock(options, name) -> bool:
    load_lockfile(options)

    git, _ = list(filter(lambda x: name in x[1], options.template.items()))[0]

    commit_hash = git_get_hash(get_work_dir(git))

    return globals()['LOCKFILE_SAV'][name] == commit_hash
