import functools
import sys
import nose
from preparation.resources.Resource import trunks_registered, applied_modifiers, resource_by_trunk

__author__ = 'moskupols'

_multiprocess_shared_ = True

_all_trunks = set(trunks_registered())
_trunk_filter = _all_trunks


def trunk_parametrized(trunks=set(trunks_registered())):
    def decorate(tester):
        @functools.wraps(tester)
        def generate_tests(*args):
            for t in _trunk_filter & trunks:
                yield (tester, t) + args
        return generate_tests

    return decorate


@functools.lru_cache()
def asset_cache(trunk):
    return tuple(applied_modifiers(resource_by_trunk(trunk)()))


def main(args=None):
    global _trunk_filter

    if args is None:
        args = sys.argv

    include = _all_trunks & set(args)
    exclude_percented = set('%' + t for t in _all_trunks) & set(args)
    exclude = set(e[1:] for e in exclude_percented)

    if len(include) == 0:
        include = _all_trunks
    _trunk_filter = include - exclude

    args = [arg for arg in args if arg not in include | exclude_percented]
    nose.main(argv=args)
