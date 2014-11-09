import argparse

__author__ = 'moskupols'


def evolution(title=None, resource=None, *, modifiers=None, explanations=None):
    from copy import copy
    from hb_res.explanations import Explanation
    from preparation.resources.Resource import resource_by_name

    def evolute(start, mods):
        cur = copy(start)
        yield (None, cur)
        for m in mods:
            cur = m(cur)
            yield (m, cur)
            if cur is None:
                break

    if isinstance(resource, str):
        resource = resource_by_name(resource)()

    assert modifiers is not None or hasattr(resource, 'modifiers')
    if modifiers is None:
        modifiers = resource.modifiers

    assert (title is not None and resource is not None) ^ (explanations is not None)
    if explanations is None:
        explanations = filter(lambda e: e.title == title, resource)

    if isinstance(explanations, Explanation):
        return tuple(evolute(explanations, modifiers))
    else:
        for start_expl in explanations:
            yield (start_expl, tuple(evolute(start_expl, modifiers)))


def make_argparser():
    from preparation.resources.Resource import names_registered

    parser = argparse.ArgumentParser(description='View how some explanation(s) evolute ')

    formats = {
        'oneline': '{mod!s:>50} -> ("{result.title}" := "{result.text}")',
        'wide': '{mod!s:>60} -> {result!r}',
        'twoline': 'after {mod}:\n --> {result!r}'
    }

    fmt_args = parser.add_mutually_exclusive_group()
    fmt_args.add_argument('--format',
                          default=formats['twoline'],
                          help='''Self argument for str.format call while printing evolution.
                          If omitted, same as --twoline.
                          ''')
    for name, fmt in formats.items():
        fmt_args.add_argument('--' + name,
                              dest='format',
                              action='store_const',
                              const=fmt,
                              help='Format as ' + repr(fmt))

    parser.add_argument('resource',
                        choices=names_registered(),
                        help='resource to use')
    parser.add_argument('title',
                        nargs='+',
                        help='''title (titles) to show.
                        They will be used to find raw explanations yielded by the resource's parser,
                        so should be exactly in the same format the parser gives it.''')
    return parser


def main(args=None):
    if not isinstance(args, argparse.Namespace):
        parser = make_argparser()
        args = parser.parse_args(args)
    first_story = True
    for title in args.title:
        stories = evolution(title=title, resource=args.resource)
        for start_expl, story in stories:
            if first_story:
                first_story = False
            else:
                print()
            for mod, result in story:
                print(args.format.format(mod=mod, result=result))


if __name__ == '__main__':
    main()
