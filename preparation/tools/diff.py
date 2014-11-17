__author__ = 'pershik'

from preparation.resources.Resource import resource_by_name
from hb_res.storage import get_storage

import difflib
import argparse


def diff(resource_name=None, modifiers=None):

    assert isinstance(resource_name, str)
    resource = resource_by_name(resource_name + 'Resource')()

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

    with get_storage(resource_name) as old_explanations:
        new_explanations = list(filter(lambda x: x is not None, map(apply(modifiers), resource)))
        return difflib.unified_diff(list(old_explanations.entries()), new_explanations)


def make_argparser():
    from preparation.resources.Resource import names_registered

    parser = argparse.ArgumentParser(description='View how some resource changes')

    trunks = [name.replace('Resource', '') for name in names_registered()]

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