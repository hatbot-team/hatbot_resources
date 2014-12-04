__author__ = 'ryad0m'

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/data.txt'

__all__ = ['parse_ngram']

from . import parse_ngram
