__author__ = 'shkiper'

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/crosswords.txt'

__all__ = ['parse_crosswords']

from . import parse_crosswords