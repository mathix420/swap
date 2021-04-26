import argparse
from .config import get_config

from swap.handlers.remove import remove_component
from swap.handlers.sync import sync_component
from swap.handlers.add import add_component
from swap.handlers.get import get_component
from swap.handlers.tree import tree_view
from swap.handlers.init import init_app


parser = argparse.ArgumentParser('swp')
parser.add_argument('-c', metavar='PATH', type=str, help="Configuration path", default="swap.yaml")
parser.add_argument('-l', metavar='PATH', type=str, help="Lockfile path", default="swap.lock")

# SUBPARSER CONFIG
subparser = parser.add_subparsers(
    dest='action', title='action', description='SWAP actions', required=True)

# INIT
init = subparser.add_parser('init', help='initialize a new project')
init.set_defaults(handler=init_app, require_config=False)

# TREE
tree = subparser.add_parser('tree', help='show tree view of remotes')
tree.set_defaults(handler=tree_view, require_config=True)

# SYNC
sync = subparser.add_parser('sync', help='sync components')
sync.add_argument('NAME', nargs='*', help='component(s) to sync')
sync.add_argument('-m', '--commit-msg', help='commit message')
sync.add_argument('-f', '--force', action='store_true', help='force pushing updates')
sync.set_defaults(handler=sync_component, require_config=True)

# ADD
add = subparser.add_parser('add', help='add component to the project')
add.add_argument('PATH', help='path of the component')
add.add_argument('DEST', nargs='?', help='path of the remote component')
add.add_argument('REMOTE', help='git remote url')
add.add_argument('-n', '--name', nargs='?', help='name of the component')
add.set_defaults(handler=add_component, require_config=True)

# GET
get = subparser.add_parser('get', help='get component locally from remote')
get.add_argument('PATH', help='remote path of the component')
get.add_argument('DEST', nargs='?', help='local path of the component')
get.add_argument('REMOTE', help='git remote url')
get.add_argument('-n', '--name', nargs='?', help='name of the component')
get.set_defaults(handler=get_component, require_config=True)

# REMOVE
remove = subparser.add_parser('rm', help='remove component from the project')
remove.add_argument('NAME', help='path of the component')
remove.set_defaults(handler=remove_component, require_config=True)


def main():
    # Parse arguments
    options = parser.parse_args()

    # Load local config
    try:
        options.template = get_config(options.c)
    except:
        options.template = None

    # Check if local config is required
    if options.require_config and not options.template:
        exit('You should have init a project before running this command')

    # Execute the command
    if options.handler:
        options.handler(options)
