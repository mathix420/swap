from swap.config import save_config, get_config
from swap.handlers.sync import sync_component
from swap.git import init_git, has_git

from argparse import Namespace
from PyInquirer import prompt
from termcolor import cprint
from os import path


demo = '''\
# Here is the remote url (can be anything as long as git can handle it)
https://github.com/mathix420/swap.git:
  # component_name: local_path:remote_path
  example: example.md:doc/guide.md

# optionnaly you can add a git identifier at the end of the remote path
# like so:
#  example: example.md:doc/guide.md@commit_id
#  example: example.md:doc/guide.md@branch_name

# Open the example.md file to know more about swap

# If you want to remove this file type these commands
#  swp rm example
#  rm example.md
'''


def get_demo():
    return prompt({
        'type': 'confirm',
        'name': 'continue',
        'default': False,
        'message': 'Use a demo swapfile',
    })['continue']


def git_init_ok():
    return prompt({
        'type': 'confirm',
        'name': 'continue',
        'default': True,
        'message': 'SWAP require a git project, can we run `git init`',
    })['continue']


def add_component(new=False):
    return prompt({
        'type': 'confirm',
        'name': 'continue',
        'default': False,
        'message': f'Add a{" new " if new else " "}component',
    })['continue']


def get_path(local=True):
    return prompt({
        'type': 'input',
        'name': 'folder',
        'default': './',
        'message': 'Local path' if local else 'Remote path',
    })['folder']


def get_remote_url():
    res = ''
    while not res:
        res = prompt({
            'type': 'input',
            'name': 'remote',
            'message': 'Remote url (git)',
        })['remote']
    return res


def init_app(options: Namespace):
    config = {}

    if path.exists(options.c):
        exit('Cannot override existing configuration')

    if not has_git('.'):
        if git_init_ok():
            init_git('.')
        else:
            quit('SWAP require a git project!')

    while add_component(bool(config)):
        local_path = get_path()
        remote_path = get_path(False)
        remote_url = get_remote_url()
        name = path.basename(local_path)

        if not remote_url in config:
            config[remote_url] = {name: f'{local_path}:{remote_path}'}
        else:
            config[remote_url][name] = f'{local_path}:{remote_path}'

    if not config and get_demo():
        with open(options.c, 'w+') as fp:
            fp.write(demo)
        options.template = get_config(options.c)
        options.force = True
        options.NAME = None
        sync_component(options, skip_checks=True, no_commit=True)
    else:
        save_config(config, options.c)
    cprint('All done 🚀', 'green')
    print('Commit and run `swp sync` when ready!')
