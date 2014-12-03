from copy import copy
import argparse

from preparation.resources.Resource import names_registered, resource_by_name
from hb_res.storage import get_storage, ExplanationStorage

def rebuild_trunk(trunk: str):
    resource_by_name(trunk + 'Resource')().build()

def get_names():
    return [name.replace('Resource', '') for name in names_registered()]

def make_argparser():
    parser = argparse.ArgumentParser(description='Rebuild some asset')

    names = get_names()

    parser.add_argument('resources',
                        metavar='RESOURCE',
                        nargs='+',
                        choices=names + ['all'],
                        help='One of registered resources ({}) or just \'all\'.'.format(', '.join(names)))

    return parser


def main(args=None):
    if not isinstance(args, argparse.Namespace):
        parser = make_argparser()
        args = parser.parse_args(args)
    assert not ('all' in args.resources and len(args.resources) != 1)
    if 'all' in args.resources:
        for name in get_names():
            rebuild_trunk(name)
    else:
        for name in args.resources:
            rebuild_trunk(name)


if __name__ == '__main__':
    main()
