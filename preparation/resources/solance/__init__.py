__author__ = 'pershik'

import os

__all__ = ['extractor', 'extract_from_solance']

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/solance_raw.txt'

from . import parse_solance
