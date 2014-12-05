import unittest
import nose

__author__ = 'moskupols'

from preparation.resources import Resource
from tests.trunk_aware import trunk_parametrized, asset_cache


@trunk_parametrized()
def test_determinacy(trunk):
    resource_class = Resource.resource_by_trunk(trunk)

    r1, r2 = asset_cache(trunk), tuple(Resource.applied_modifiers(resource_class()))
    unittest.TestCase().assertTupleEqual(r1, r2)


if __name__ == '__main__':
    nose.main()
