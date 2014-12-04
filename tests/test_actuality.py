import unittest
import nose
from tests.trunk_aware import trunk_parametrized
from hb_res.storage import get_storage
from preparation.resources.Resource import resource_by_trunk, applied_modifiers

__author__ = 'moskupols'


@trunk_parametrized()
def test_actuality(trunk):
    with get_storage(trunk) as storage:
        stored = tuple(storage.entries())
    actual = tuple(applied_modifiers(resource_by_trunk(trunk)()))
    unittest.TestCase().assertSequenceEqual(stored, actual)


if __name__ == '__main__':
    nose.main()
