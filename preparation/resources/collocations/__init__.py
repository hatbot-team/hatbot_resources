__author__ = 'shkiper'

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/collocations.txt'

__all__ = ['parse_collocations']

from . import parse_collocations