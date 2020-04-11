from .git import git_clone, git_pull, git_push, git_add_commit
from .questions import get_remote_url, get_sub_folder
from .config import save_config
from .tree import list_files

from distutils.dir_util import copy_tree
from shutil import copy2
from os import path


def get_work_dir(config):
    folder = config['remote'].split('/')[-1].split('.')[0]
    return path.join('/tmp', folder)


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
        'remote-directory': get_sub_folder(options),
        'components': {},
    }

    save_config(config, options.c)
    git_clone(config['remote'], get_work_dir(config))


def tree_view(options):
    work_dir = get_work_dir(options.config)
    subdest = path.join(work_dir, options.config['remote-directory'])
    list_files(subdest)


def push_app(options):
    work_dir = get_work_dir(options.config)
    subdest = path.join(work_dir, options.config['remote-directory'])

    if not path.exists(work_dir):
        git_clone(options.config['remote'], work_dir)
    else:
        git_pull(work_dir)

    for name, item_path in options.config['components'].items():
        if path.isdir(item_path):
            copy_tree(item_path, path.join(subdest, name))
        else:
            copy2(item_path, path.join(subdest, name))

    git_add_commit(work_dir, options.MESSAGE or None)
    git_push(work_dir)


def pull_components(options):
    # TODO: Detect unvalidated changes in git and ask if it's ok
    work_dir = get_work_dir(options.config)
    subdest = path.join(work_dir, options.config['remote-directory'])

    if not path.exists(work_dir):
        git_clone(options.config['remote'], work_dir)
    else:
        git_pull(work_dir)

    for name, item_path in options.config['components'].items():
        if path.isdir(path.join(subdest, name)):
            copy_tree(path.join(subdest, name), item_path)
        else:
            copy2(path.join(subdest, name), item_path)


def add_component(options):
    for item in options.PATH:
        check_path(item)
        name = path.basename(item)
        if name not in options.config['components']:
            options.config['components'][name] = path.normpath(item)
        else:
            print('Cannot add 2 component with the same name')
    save_config(options.config, options.c)


def get_component(options):
    work_dir = get_work_dir(options.config)
    subdest = path.join(work_dir, options.config['remote-directory'])
    name = options.NAME
    dest = options.DEST

    if not path.exists(work_dir):
        git_clone(options.config['remote'], work_dir)
    else:
        git_pull(work_dir)

    if path.exists(dest):
        exit(f'This path already exists {dest}')
    if not path.exists(path.join(subdest, name)):
        exit(f'No components found for this name {name}')
    if path.isdir(path.join(subdest, name)):
        copy_tree(path.join(subdest, name), dest)
    else:
        copy2(path.join(subdest, name), dest)


def remove_component(options):
    for item in options.PATH:
        check_path(item)
        if path.basename(item) in options.config['components']:
            options.config['components'].pop(path.basename(item))
        else:
            print(f'Cannot find the component {path.basename(item)}')
    save_config(options.config, options.c)
