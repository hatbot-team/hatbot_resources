import re
import unittest
import nose
from tests.trunk_aware import trunk_parametrized, asset_cache

__author__ = 'moskupols'

GOOD_TITLE_RE = re.compile(r'^([ёа-я]{2,}|[ёа-я]{2,}-[ёа-я]{2,})$')


@trunk_parametrized()
def test_title_well_formed(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        case.assertRegex(e.title, GOOD_TITLE_RE, msg=repr(e))


if __name__ == '__main__':
    nose.main()

