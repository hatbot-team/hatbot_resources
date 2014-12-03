import argparse
from preparation.resources.Resource import trunks_registered, resource_by_trunk, resource_build


def make_argparser():
    parser = argparse.ArgumentParser(description='Rebuild some asset')

    names = tuple(trunks_registered())

    parser.add_argument('resources',
                        metavar='RESOURCE',
                        nargs='+',
                        choices=names + ('all',),
                        help='One of registered resources ({}) or just \'all\'.'.format(', '.join(names)))

    return parser


def main(args=None):
    if not isinstance(args, argparse.Namespace):
        parser = make_argparser()
        args = parser.parse_args(args)
    assert not ('all' in args.resources and len(args.resources) != 1)
    if 'all' in args.resources:
        args.resources = trunks_registered()
    for name in args.resources:
        resource_by_trunk(name)().build()


if __name__ == '__main__':
    main()
