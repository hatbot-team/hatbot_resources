__author__ = 'moskupols'

from preparation.resources import Resource
from tests.trunk_aware import TrunkAwareTestCase, trunk_aware_run


class DeterminacyTestCase(TrunkAwareTestCase):
    def _test_trunk(self):
        resource_class = Resource.resource_by_trunk(self.trunk)

        r1, r2 = resource_class(), resource_class()
        self.assertSequenceEqual(*(tuple(Resource.applied_modifiers(r) for r in (r1, r2))))


if __name__ == '__main__':
    trunk_aware_run(DeterminacyTestCase)
