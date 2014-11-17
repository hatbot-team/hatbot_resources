__author__ = 'Алексей'

import os

__all__ = ['import_from_site', 'parse_synonyms']

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/synonyms_raw.txt'

from . import parse_synonyms