import json
from .git import git_get_hash
from os.path import join, isdir
from collections import ChainMap
from subprocess import check_output


def get_current_hash(path):
    if isdir(path):
        e = check_output(
            f'find -s {path} -type f -exec md5sum {{}} \\; | md5sum', shell=True)
    else:
        e = check_output(f'md5sum {path}', shell=True)
    return e.decode('utf-8').split(' ')[0]


def get_lock(name):
    try:
        with open('swap-lock.json') as fp:
            return json.load(fp)
    except IOError as e:
        if e.errno != 2:
            raise e
        return {}


def get_hashes(options, name):
    for remote, values in options.template.items():
        if not values.get(name): continue
        path = join('/tmp/', remote.split('/')[-1].split('.')[0])
        out, _ = values.get(name).split(':')

    return {
        'current_version': git_get_hash(path),
        'last_hash': get_current_hash(out)
    }


def update_lock(options, name):
    j = get_lock(name)
    tmp = j.copy()  # save to check for changes

    j[name] = get_hashes(options, name)

    with open('swap-lock.json', 'w') as fp:
        json.dump(j, fp, indent=4, sort_keys=True)

    return tmp == j


def check_lock(options, name):
    j = get_lock(name)
    tmp = j.copy()  # save to check for changes

    j[name] = get_hashes(options, name)

    return tmp == j
