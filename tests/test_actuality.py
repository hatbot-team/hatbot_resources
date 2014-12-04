from tests.trunk_aware import TrunkAwareTestCase, trunk_aware_main
from hb_res.storage import get_storage
from preparation.resources.Resource import resource_by_trunk, applied_modifiers

__author__ = 'moskupols'


class ActualityTestCase(TrunkAwareTestCase):
    def _test_trunk_actuality(self):
        trunk = self.trunk
        stored = tuple(get_storage(trunk).entries())
        actual = tuple(applied_modifiers(resource_by_trunk(trunk)()))
        self.assertSequenceEqual(stored, actual)


if __name__ == '__main__':
    trunk_aware_main(ActualityTestCase)
