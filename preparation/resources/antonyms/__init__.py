__author__ = 'Алексей'

__all__ = ['parse_antonyms']

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/antonyms_raw.txt'

from . import parse_antonyms