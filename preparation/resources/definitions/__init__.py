__author__ = 'skird'

import os

__all__ = ['parse_definitions']

PREFIX = os.path.dirname(os.path.abspath(__file__))
_raw_data = PREFIX + '/raw_data/definitions.txt'

from . import parse_definitions
