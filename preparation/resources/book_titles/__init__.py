__author__ = 'shkiper'

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/book_titles.txt'

__all__ = ['parse_book_titles']

from . import parse_book_titles
