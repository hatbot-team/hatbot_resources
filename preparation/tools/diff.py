__author__ = 'pershik'

from preparation.resources.Resource import resource_by_trunk
from hb_res.storage import get_storage

import difflib
import argparse


def diff(trunk=None, modifiers=None):

    assert isinstance(trunk, str)
    resource = resource_by_trunk(trunk)()

    if modifiers is None:
        modifiers = resource.modifiers

    def apply(modifiers):
        def func(expl):
            for modifier in modifiers:
                if expl is None:
                    break
                expl = modifier(expl)
            return expl
        return func

    with get_storage(trunk) as old_explanations:
        new_explanations = list(map(str, filter(lambda x: x is not None, map(apply(modifiers), resource))))
        return difflib.unified_diff(list(map(str, old_explanations.entries())), new_explanations)


def make_argparser():
    from preparation.resources.Resource import trunks_registered

    parser = argparse.ArgumentParser(description='View how some resource changes')

    trunks = trunks_registered()

    parser.add_argument('resource',
                        metavar='RESOURCE',
                        choices=trunks,
                        help='One of registered resources ({})'.format(', '.join(trunks)))
    return parser


def main(args=None):
    if not isinstance(args, argparse.Namespace):
        parser = make_argparser()
        args = parser.parse_args(args)
    for entry in diff(args.resource):
        print(entry)

if __name__ == '__main__':
    main()
