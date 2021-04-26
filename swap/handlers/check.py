from swap.lock import check_lock

from argparse import Namespace
from termcolor import colored
from itertools import chain


def check(options: Namespace):
    to_check = options.NAME
    if not to_check:
        to_check = list(chain.from_iterable(
            x.keys() for x in options.template.values()
        ))
    res = [check_lock(options, name) for name in to_check]
    if all(res):
        return print("All is good nothing has changed")
    for i, r in filter(lambda x: not x[1], enumerate(res)):
        print(colored(to_check[i], 'red'), 'has changed since last sync.')
