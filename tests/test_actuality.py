import unittest
import nose
from tests.trunk_aware import trunk_parametrized, asset_cache
from hb_res.storage import get_storage

__author__ = 'moskupols'


@trunk_parametrized()
def test_actuality(trunk):
    with get_storage(trunk) as storage:
        stored = tuple(storage.entries())
    actual = asset_cache(trunk)
    unittest.TestCase().assertSequenceEqual(stored, actual)


if __name__ == '__main__':
    nose.main()
