from swap.utils import check_path, get_remote_path
from swap.config import save_config

from argparse import Namespace
from os import path


def add_component(options: Namespace):
    work_dir = get_remote_path(options.REMOTE)
    remote_path = path.join(work_dir, options.PATH)
    check_path(remote_path)

    local_path = options.DEST or path.normpath(options.PATH)
    name = options.name or path.basename(local_path)

    if name not in options.template[options.REMOTE]:
        options.template[options.REMOTE][name] = local_path + ':' + \
            path.normpath(options.PATH)
    else:
        exit('Cannot add 2 component with the same name')
    save_config(options.template, options.c)
    return name
