__author__ = 'moskupols'

import unittest
from tests.trunk_aware import trunk_aware_main

loader = unittest.TestLoader()
tests = loader.discover('.')
trunk_aware_main(tests)
