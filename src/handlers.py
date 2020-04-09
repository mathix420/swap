from .git import git_clone, git_pull, git_push, git_add_commit
from .remote import get_remote_url
from .config import save_config

from distutils.dir_util import copy_tree
from shutil import copy2
from os import path


def check_path(item):
    if path.isfile(item):
        return True
    elif path.isdir(item):
        return True
    exit('You must choose a file or a directory')


def init_app(options):
    if path.exists(options.c):
        exit('Cannot override existing configuration')

    config = {
        'version': 1,
        'remote': get_remote_url(options),
        # TODO: add config for this
        'remote-directory': '.',
        'components': {},
    }

    save_config(config, options.c)


def push_app(options):
    dest = '/tmp/swp_test'

    if not path.exists(dest):
        git_clone(options.config['remote'], dest)
    else:
        git_pull(dest)

    for name, item_path in options.config['components'].items():
        if path.isdir(item_path):
            copy_tree(item_path, path.join(dest, name))
        else:
            copy2(item_path, path.join(dest, name))

    git_add_commit(dest, options.MESSAGE or None)
    git_push(dest)


def pull_components(options):
    # TODO: Detect unvalidated changes in git and ask if it's ok
    dest = '/tmp/swp_test'

    if not path.exists(dest):
        git_clone(options.config['remote'], dest)
    else:
        git_pull(dest)

    for name, item_path in options.config['components'].items():
        if path.isdir(item_path):
            copy_tree(path.join(dest, name), item_path)
        else:
            copy2(path.join(dest, name), item_path)


def add_component(options):
    for item in options.PATH:
        check_path(item)
        name = path.basename(item)
        if name not in options.config['components']:
            options.config['components'][name] = path.normpath(item)
        else:
            print('Cannot add 2 component with the same name')
    save_config(options.config, options.c)


def remove_component(options):
    for item in options.PATH:
        check_path(item)
        if path.basename(item) in options.config['components']:
            options.config['components'].pop(path.basename(item))
        else:
            print(f'Cannot find the component {path.basename(item)}')
    save_config(options.config, options.c)
