from copy import copy
import argparse

from preparation.resources.Resource import names_registered, resource_by_name
from hb_res.storage import get_storage, ExplanationStorage


def generate_asset(resource, out_storage: ExplanationStorage):
    out_storage.clear()
    total, yielded = 0, 0
    for explanation in resource:
        total += 1
        r = copy(explanation)
        for functor in resource.modifiers:
            if r is None:
                break
            r = functor(r)
        if r is not None:
            out_storage.add_entry(r)
            yielded += 1
    return yielded, total


def rebuild_trunk(trunk: str):
    resource = resource_by_name(trunk + 'Resource')()
    with get_storage(trunk) as out_storage:
        ret = generate_asset(resource, out_storage)
    return ret


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
    def pretty_build(trunk):
        import time

        print("<=> Starting {} generation".format(trunk))
        start = time.monotonic()
        yielded, total = rebuild_trunk(trunk)
        end = time.monotonic()
        print("> {} generated in {} seconds".format(name, end - start))
        print("> {} explanations out of {} raw entries have passed the filters".format(yielded, total))

    if not isinstance(args, argparse.Namespace):
        parser = make_argparser()
        args = parser.parse_args(args)
    assert not ('all' in args.resources and len(args.resources) != 1)
    if 'all' in args.resources:
        for name in get_names():
            pretty_build(name)
    else:
        for name in args.resources:
            pretty_build(name)


if __name__ == '__main__':
    main()
