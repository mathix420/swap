from .utils import get_work_dir
from .git import git_get_hash

import json


global LOCKFILE
LOCKFILE = dict()


def load_lockfile(options) -> "dict[str, dict[str, str]]":
    if not globals()['LOCKFILE']:
        try:
            with open(options.l) as fp:
                globals()['LOCKFILE'] = json.load(fp)
        except IOError as e:
            if e.errno != 2:
                raise e
            globals()['LOCKFILE'] = {
                "0": 'Auto-generated file, do not edit nor delete!',
                "1": 'This file should be present in your version control system.'
            }

    return globals()['LOCKFILE']


def save_lockfile(options):
    with open(options.l, 'w') as fp:
        json.dump(globals()['LOCKFILE'], fp, indent=4, sort_keys=True)


def get_hash(options, name: str) -> "dict[str, str]":
    return load_lockfile(options).get(name, {})


def update_lock(options, git_url: str) -> bool:
    has_changed = False
    load_lockfile(options)
    commit_hash = git_get_hash(get_work_dir(git_url))
    local_commit = git_get_hash('.')

    for component_name in options.template.get(git_url).keys():
        current = (globals()['LOCKFILE'].get(
            component_name, {}).get('remote') != commit_hash)
        has_changed = has_changed or current

        if current:
            globals()['LOCKFILE'][component_name] = {
                'remote': commit_hash,
                'local': local_commit
            }

    save_lockfile(options)
    return has_changed


def check_lock(options, name) -> bool:
    load_lockfile(options)

    git, _ = list(filter(lambda x: name in x[1], options.template.items()))[0]

    commit_hash = git_get_hash(get_work_dir(git))

    return globals()['LOCKFILE'].get(name, {}).get('remote') == commit_hash
