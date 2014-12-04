import functools
import sys
import nose
from preparation.resources.Resource import trunks_registered

__author__ = 'moskupols'

_all_trunks = set(trunks_registered())
_trunk_filter =_all_trunks


def trunk_parametrized(trunks=set(trunks_registered())):
    def decorate(tester):
        @functools.wraps(tester)
        def generate_tests(*args):
            for t in _trunk_filter & trunks:
                yield (tester, t) + args
        return generate_tests

    return decorate


def main(args=None):
    global _trunk_filter

    if args is None:
        args = sys.argv

    _trunk_filter = _all_trunks & set(args)
    if len(_trunk_filter) == 0:
        _trunk_filter = _all_trunks

    args = [arg for arg in args if arg not in _trunk_filter]
    nose.main(argv=args)
