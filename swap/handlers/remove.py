from swap.lock import load_lockfile, save_lockfile
from swap.config import save_config
from swap.git import git_add_commit

from argparse import Namespace


def remove_component(options: Namespace):
    name = options.NAME

    results = list(filter(lambda x: name in x[1], options.template.items()))
    if not results:
        exit(f'Cannot find the component {name}')
    else:
        results[0][1].pop(name)
        load_lockfile(options).pop(name)
        save_lockfile(options)

    save_config(options.template, options.c)

    try:
        git_add_commit('.', f'[SWAP] REMOVE `{name}` from swap file')
    except:
        exit('Commit failed!')
