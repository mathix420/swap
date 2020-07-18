from .git import (
    git_add_commit,
    git_checkout,
    git_porcelain,
    git_clone,
    git_pull,
    git_push,
)
from .questions import get_remote_url, get_sub_folder
from .config import save_config
from .tree import list_files

from distutils.dir_util import copy_tree
from shutil import copy2, rmtree
from os import path, makedirs
import tempfile

def get_work_dir(remote):
    folder = remote.split('/')[-1].split('.')[0]
    return path.join(tempfile.gettempdir(), folder)


def split_path(string):
    out_path, in_path = string.split(':')
    if '@' in in_path:
        in_path, commit_id = in_path.split('@')
    else:
        commit_id = None
    return out_path, in_path, commit_id


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
    work_dir = get_work_dir(options.template)
    subdest = path.join(work_dir, options.template['remote-directory'])
    list_files(subdest)


def push_app(options):
    for remote, modules in options.template.items():
        work_dir = get_work_dir(remote)

        if not path.exists(work_dir):
            git_clone(remote, work_dir)
        else:
            git_pull(work_dir)

        for _name, p in modules.items():
            out_path, in_path, commit_id = split_path(p)
            if commit_id:
                continue
            if path.isdir(out_path):
                rmtree(path.join(work_dir, in_path))
                makedirs(path.join(work_dir, in_path), exist_ok=True)
                copy_tree(out_path, path.join(work_dir, in_path))
            else:
                copy2(out_path, path.join(work_dir, in_path))

        try:
            git_add_commit(work_dir, options.MESSAGE or None)
            git_push(work_dir)
        except:
            pass


def pull_components(options):
    # TODO: Multithreading
    if git_porcelain('.'):
        exit('Please clean your working tree.')
    for remote, modules in options.template.items():
        work_dir = get_work_dir(remote)

        if not path.exists(work_dir):
            git_clone(remote, work_dir)
        else:
            git_pull(work_dir)

        for _name, p in modules.items():
            out_path, in_path, commit_id = split_path(p)
            if commit_id:
                git_checkout(work_dir, commit_id)
            if path.isdir(path.join(work_dir, in_path)):
                rmtree(out_path)
                makedirs(out_path, exist_ok=True)
                copy_tree(path.join(work_dir, in_path), out_path)
            else:
                copy2(path.join(work_dir, in_path), out_path)
            if commit_id:
                git_checkout(work_dir, 'master')


def add_component(options):
    for item in options.PATH:
        check_path(item)
        name = path.basename(item)
        if name not in options.template['components']:
            options.template['components'][name] = path.normpath(item)
        else:
            print('Cannot add 2 component with the same name')
    save_config(options.template, options.c)


def get_component(options):
    work_dir = get_work_dir(options.template)
    subdest = path.join(work_dir, options.template['remote-directory'])
    name = options.NAME
    dest = options.DEST

    if not path.exists(work_dir):
        git_clone(options.template['remote'], work_dir)
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
        if path.basename(item) in options.template['components']:
            options.template['components'].pop(path.basename(item))
        else:
            print(f'Cannot find the component {path.basename(item)}')
    save_config(options.template, options.c)
