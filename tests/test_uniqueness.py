import unittest
import nose
from tests.trunk_aware import trunk_parametrized, asset_cache

__author__ = 'moskupols'


@trunk_parametrized()
def test_uniqueness(trunk):
    asset = tuple((e.title, e.text, e.key) for e in asset_cache(trunk))
    unittest.TestCase().assertCountEqual(asset, set(asset))


if __name__ == '__main__':
    nose.main()
