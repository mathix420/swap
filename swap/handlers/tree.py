from swap.utils import get_work_dir

from argparse import Namespace
from os import path, walk, sep
import subprocess


def list_files(startpath):
    if path.exists('/bin/tree'):
        subprocess.run(f'/bin/tree {startpath}', shell=True)
        return

    for root, _, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = ' ' * 2 * (level)
        if '.git' in root:
            continue
        print('{}{}/'.format(indent, path.basename(root)))
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def tree_view(options: Namespace):
    work_dir = get_work_dir(options.template)
    subdest = path.join(work_dir, options.template['remote-directory'])
    list_files(subdest)
