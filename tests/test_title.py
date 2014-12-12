import unittest
import nose

from tests.trunk_aware import trunk_parametrized, asset_cache
from preparation.lang_utils.morphology import looks_like_valid_russian, TYPICAL_RUSSIAN_RE
from preparation.blacklists import TITLE_BLACKLIST

__author__ = 'moskupols'

@trunk_parametrized()
def test_title_well_formed(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        if not looks_like_valid_russian(e.title):
            msg = repr(e)
            if e.title in TITLE_BLACKLIST:
                msg += ' (blacklisted)'
            if not TYPICAL_RUSSIAN_RE.match(e.title):
                msg += ' (not matched by {!r})'.format(TYPICAL_RUSSIAN_RE)
            case.assertTrue(looks_like_valid_russian(e.title), msg=msg)

if __name__ == '__main__':
    nose.main()

