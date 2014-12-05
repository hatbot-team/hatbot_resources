import functools
import random
import sys
import nose
import hb_res
from preparation.resources.Resource import trunks_registered, applied_modifiers, resource_by_trunk

__author__ = 'moskupols'

_multiprocess_shared_ = True

_all_trunks = set(trunks_registered())
_trunk_filter = _all_trunks


def trunk_parametrized(trunks=_all_trunks):
    def decorate(tester):
        @functools.wraps(tester)
        def generate_tests(*args):
            interesting = list(_trunk_filter & set(trunks))
            random.shuffle(interesting)
            for t in interesting:
                yield (tester, t) + args
        return generate_tests

    return decorate

_use_generated = False


@functools.lru_cache()
def asset_cache(trunk):
    if _use_generated and trunk in hb_res.storage.list_storages():
        with hb_res.storage.get_storage(trunk) as storage:
            ret = tuple(storage.entries())
        return ret
    return tuple(applied_modifiers(resource_by_trunk(trunk)()))


def main(args=None):
    global _trunk_filter, _use_generated

    if args is None:
        args = sys.argv

    include = _all_trunks & set(args)
    exclude_percented = set('%' + t for t in _all_trunks) & set(args)
    exclude = set(e[1:] for e in exclude_percented)

    if len(include) == 0:
        include = _all_trunks
    _trunk_filter = include - exclude

    _use_generated = '--use-generated' in args

    args = [arg for arg in args if arg not in include | exclude_percented | {'--use-generated'}]
    nose.main(argv=args)
