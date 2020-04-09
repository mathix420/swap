from .config import save_config
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
    save_config({'version': 1, 'components': {}}, options.c)


def push_app(options):
    pass


def add_component(options):
    for item in options.PATH:
        check_path(item)
        if path.basename(item) not in options.config['components']:
            options.config['components'][path.basename(item)] = path.normpath(item)
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

