__author__ = 'shkiper'

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/phraseologism.txt'

__all__ = ['parse_phraseological']

from . import parse_phraseological