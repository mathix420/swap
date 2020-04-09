import argparse
from .config import get_config
from .handlers import (
    remove_component,
    pull_components,
    add_component,
    get_component,
    tree_view,
    init_app,
    push_app,
)

parser = argparse.ArgumentParser('swp')
parser.add_argument('-c', metavar='PATH', type=str, help="Configuration path", default="swap.yaml")

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

# PUSH
push = subparser.add_parser('push', help='push components to remote')
push.add_argument('MESSAGE', nargs='?', help='commit message')
push.set_defaults(handler=push_app, require_config=True)

# PULL
pull = subparser.add_parser('pull', help='pull components from remote')
pull.set_defaults(handler=pull_components, require_config=True)

# ADD
add = subparser.add_parser('add', help='add component to the project')
add.add_argument('PATH', nargs='+', help='path of the component')
add.set_defaults(handler=add_component, require_config=True)

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
        options.config = get_config(options.c)
    except:
        options.config = None

    # Check if local config is required
    if options.require_config and not options.config:
        exit('You should have init a project before running this command')

    # Execute the command
    if options.handler:
        options.handler(options)
