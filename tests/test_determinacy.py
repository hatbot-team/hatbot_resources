__author__ = 'moskupols'

import unittest
from preparation.resources import Resource
from tests.trunk_aware import TrunkAwareTestCase, trunk_aware_run


class DeterminacyTestCase(TrunkAwareTestCase):
    def _test_trunk(self):
        resource_class = Resource.resource_by_trunk(self.trunk)

        r1, r2 = resource_class(), resource_class()
        for i, (e1, e2) in enumerate(zip(*map(Resource.applied_modifiers, (r1, r2)))):
            self.assertEqual(e1, e2)


if __name__ == '__main__':
    trunk_aware_run(unittest.defaultTestLoader.loadTestsFromTestCase(DeterminacyTestCase))
