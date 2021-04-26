from swap.questions import get_remote_url, get_sub_folder
from swap.config import save_config
from swap.utils import get_work_dir
from swap.git import git_clone

from argparse import Namespace
from os import path


def init_app(options: Namespace):
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
