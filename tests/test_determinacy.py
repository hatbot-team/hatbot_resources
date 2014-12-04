import unittest
import nose

__author__ = 'moskupols'

from preparation.resources import Resource
from tests.trunk_aware import trunk_parametrized


@trunk_parametrized()
def test_trunk(trunk):
    resource_class = Resource.resource_by_trunk(trunk)

    r1, r2 = resource_class(), resource_class()
    unittest.TestCase().assertSequenceEqual(*(tuple(Resource.applied_modifiers(r)) for r in (r1, r2)))


if __name__ == '__main__':
    nose.main()
