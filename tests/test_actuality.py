import unittest
import nose
from hb_res.storage import get_storage
from tests.trunk_aware import trunk_parametrized, asset_cache

__author__ = 'moskupols'


@trunk_parametrized()
def test_actuality(trunk):
    with get_storage(trunk) as storage:
        stored = tuple(storage.entries())
    actual = asset_cache(trunk)
    unittest.TestCase().assertTupleEqual(stored, actual)


if __name__ == '__main__':
    nose.main()
