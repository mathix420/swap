from swap.handlers.sync import sync_component
from swap.handlers.add import add_component
from swap.git import git_add_commit
from swap.config import get_config

from argparse import Namespace
from os import path


def get_component(options: Namespace):
    name = add_component(options)
    options.template = get_config(options.c)
    try:
        git_add_commit('.', f'[SWAP] ADD `{name}` to swap file')
    except:
        return
    sync_component(Namespace(**{
        **options.__dict__,
        'NAME': [name or path.normpath(options.PATH)],
        'force': False,
        'commit_msg': f'[SWAP] PULL `{name}` from remote'
    }), skip_checks=True)
