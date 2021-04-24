import argparse
from .config import get_config
from .handlers import (
    remove_component,
    sync_component,
    add_component,
    get_component,
    tree_view,
    init_app,
    check,
)

parser = argparse.ArgumentParser('swp')
parser.add_argument('-c', metavar='PATH', type=str, help="Configuration path", default="swap.yaml")
parser.add_argument('-l', metavar='PATH', type=str, help="Lockfile path", default="swap.lock")

# SUBPARSER CONFIG
subparser = parser.add_subparsers(
    dest='action', title='action', description='SWAP actions', required=True)

# INIT
init = subparser.add_parser('init', help='initialize a new project')
init.add_argument('--remote', '-r', help='git repository url')
init.add_argument('--folder', '-f', help='subfolder path')
init.set_defaults(handler=init_app, require_config=False)

# TREE
tree = subparser.add_parser('tree', help='show tree view of remote')
tree.set_defaults(handler=tree_view, require_config=True)

# SYNC
sync = subparser.add_parser('sync', help='sync components')
sync.add_argument('NAME', nargs='*', help='component(s) to sync')
sync.add_argument('-m', '--commit-msg', help='commit message')
sync.add_argument('-f', '--force', help='force pushing updates')
sync.set_defaults(handler=sync_component, require_config=True)

# ADD
add = subparser.add_parser('add', help='add component to the project')
add.add_argument('PATH', nargs='+', help='path of the component')
add.set_defaults(handler=add_component, require_config=True)

# CHECK
add = subparser.add_parser('check', help='check if component has changed')
add.add_argument('NAME', nargs='*', help='name of component to check')
add.set_defaults(handler=check, require_config=True)

# GET
get = subparser.add_parser('get', help='get component locally from remote')
get.add_argument('NAME', help='component name to get')
get.add_argument('DEST', help='path where component should be created')
get.set_defaults(handler=get_component, require_config=True)

# REMOVE
remove = subparser.add_parser('rm', help='remove component from the project')
remove.add_argument('PATH', nargs='+', help='path of the component')
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
