__author__ = 'moskupols'

import unittest
from preparation.resources import Resource


class DeterminacyTestCase(unittest.TestCase):
    @classmethod
    def add_test_for(cls, res_name: str):
        def test_some_determinacy(self: unittest.TestCase):
            resource_class = Resource.resource_by_name(res_name)
            r1, r2 = resource_class(), resource_class()
            for i, (e1, e2) in enumerate(zip(*map(Resource.applied_modifiers, (r1, r2)))):
                self.assertEqual(e1, e2, '#{i}: {e1} and {e2} differ'.format(i=i, e1=e1, e2=e2))

        setattr(cls, 'test_{}_determinacy'.format(res_name.lower()), test_some_determinacy)


for name in Resource.names_registered():
    DeterminacyTestCase.add_test_for(name)


if __name__ == '__main__':
    unittest.main()
