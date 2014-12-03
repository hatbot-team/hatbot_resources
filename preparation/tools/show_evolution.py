import argparse

__author__ = 'moskupols'


def evolution(title=None, resource=None, *, modifiers: tuple=None, explanations=None):
    """
    Generates evolution stories of given explanations or explanations with known title
    being affected by modifiers of given resource or just given modifiers.

    Each story is a tuple of pairs (modifier, result). The first element of this tuple is always
     (None, initial explanation).

    For call you should specify modifiers and explanations, but you can do it implicitly
    by specifying resource and title to seek in the resource's output.

    If explanations is specified and is instance of Explanation, the function returns evolution story.
    Otherwise it returns sequence (start_explanation, evolution story).

    :param title: title of explanation to seek in exactly the same format as generated by the resource.
    :param resource: name or resource itself.
    :param modifiers: if not specified, modifiers are taken from resource.modifiers.
    :param explanations: if not specified, explanations are taken from (e for e in resource if e.title == title).
    :return:
    """
    from copy import copy
    from hb_res.explanations import Explanation
    from preparation.resources.Resource import resource_by_trunk

    def evolute(start, mods):
        cur = copy(start)
        yield (None, cur)
        for m in mods:
            cur = m(cur)
            yield (m, cur)
            if cur is None:
                break

    if isinstance(resource, str):
        resource = resource_by_trunk(resource)()

    assert modifiers is not None or hasattr(resource, 'modifiers')
    if modifiers is None:
        modifiers = resource.modifiers

    assert (title is not None and resource is not None) ^ (explanations is not None)
    if explanations is None:
        explanations = (e for e in resource if e.title == title)

    if isinstance(explanations, Explanation):
        return tuple(evolute(explanations, modifiers))
    else:
        for start_expl in explanations:
            yield (start_expl, tuple(evolute(start_expl, modifiers)))


def make_argparser():
    from preparation.resources.Resource import trunks_registered

    parser = argparse.ArgumentParser(description='View how some explanation(s) evolute ')

    formats = {
        'oneline': '{mod!s:>50} -> ({result.title!r} := {result.text!r})',
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

    parser.add_argument('trunk',
                        choices=trunks_registered(),
                        help='resource to use')
    parser.add_argument('title',
                        nargs='+',
                        help='''title (titles) to show.
                        They will be used to find raw explanations yielded by the resource's parser,
                        so should be exactly in the same format the parser gives it.''')
    return parser


def main(args=None):
    class SafeFormatWrapper:
        def __init__(self, towrap):
            self.wrapped = towrap

        def _hooked_call(self, func):
            try:
                return func(self.wrapped)
            except AttributeError:
                return '(n/a)'

        def __repr__(self):
            return self._hooked_call(repr)

        def __str__(self):
            return self._hooked_call(str)

        def __format__(self, *args, **kwargs):
            return self._hooked_call(lambda w: w.__format__(*args, **kwargs))

        def __getattr__(self, item):
            return SafeFormatWrapper(getattr(self.wrapped, item, '({} n/a)'.format(item)))

    if not isinstance(args, argparse.Namespace):
        parser = make_argparser()
        args = parser.parse_args(args)
    first_story = True
    for title in args.title:
        stories = evolution(title=title, resource=args.trunk)
        for start_expl, story in stories:
            if first_story:
                first_story = False
            else:
                print()

            for mod, result in story:
                print(args.format.format(mod=SafeFormatWrapper(mod), result=SafeFormatWrapper(result)))


if __name__ == '__main__':
    main()
