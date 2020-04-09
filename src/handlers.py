from os import path

def init_app(options):
    pass


def push_app(options):
    pass


def add_component(options):
    for item in options.PATH:
        if path.isfile(item):
            print('file', item)
        elif path.isdir(item):
            print('dir', item)
        else:
            exit('You must choose a file or a directory')


def remove_component(options):
    print(options.PATH)

