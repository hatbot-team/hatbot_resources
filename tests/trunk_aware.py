import sys
import unittest
from preparation.resources.Resource import trunks_registered

__author__ = 'moskupols'

_trunk_filter = set(trunks_registered())


class TrunkAwareTestCaseMeta(type):

    def __new__(mcs, name, bases, dct: dict):

        trunks_supported = dct.setdefault('_trunks_supported', trunks_registered())

        dct_items = list(dct.items())

        def bind_tester(tester, trunk):
            def binded(slf):
                if trunk in _trunk_filter:
                    slf.trunk = trunk
                    tester(slf)
                else:
                    print('(skipped) ', end='')
                    sys.stdout.flush()
            return binded

        for trunk in trunks_supported:
            for mth_name, mth in dct_items:
                if mth_name.startswith('_test_trunk'):

                    tester = bind_tester(mth, trunk)
                    dct.setdefault('test_' + trunk + mth_name[len('_test_trunk'):], tester)

        return super(TrunkAwareTestCaseMeta, mcs).__new__(mcs, name, bases, dct)


class TrunkAwareTestCase(unittest.TestCase, metaclass=TrunkAwareTestCaseMeta):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.trunk = ''


def trunk_aware_run(tests, trunks=None):
    global _trunk_filter
    import sys

    if isinstance(tests, TrunkAwareTestCaseMeta):
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(tests)

    if trunks is None:
        trunks = sys.argv[1:] if len(sys.argv) != 1 else trunks_registered()
    _trunk_filter = set(trunks)

    unittest.TextTestRunner(verbosity=2).run(tests)
