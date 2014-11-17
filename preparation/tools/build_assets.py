from copy import copy
import argparse

from preparation.resources.Resource import names_registered, resource_by_name
from hb_res.storage import get_storage, ExplanationStorage


def generate_asset(resource, out_storage: ExplanationStorage):
    out_storage.clear()
    for explanation in resource:
        r = copy(explanation)
        for functor in resource.modifiers:
            if r is None:
                break
            r = functor(r)
        if r is not None:
            out_storage.add_entry(r)


def rebuild_trunk(trunk: str):
    resource = resource_by_name(trunk + 'Resource')()
    with get_storage(trunk) as out_storage:
        print("Starting {} generation".format(trunk))
        generate_asset(resource, out_storage)
        print("Finished {} generation".format(trunk))


def make_argparser():
    parser = argparse.ArgumentParser(description='Rebuild some asset')

    names = [name.replace('Resource', '') for name in names_registered()]

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
    assert all not in args.resources or len(args.resources) == 1
    for name in args.resources:
        rebuild_trunk(name)


if __name__ == '__main__':
    main()
