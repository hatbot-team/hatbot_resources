__author__ = 'moskupols'

import unittest

loader = unittest.TestLoader()
tests = loader.discover('.')
runner = unittest.TextTestRunner()
runner.run(tests)
