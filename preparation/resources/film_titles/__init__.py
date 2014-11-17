__author__ = 'shkiper'

import os

PREFIX = os.path.dirname(os.path.abspath(__file__))

_raw_data = PREFIX + '/raw_data/film_titles.txt'

__all__ = ['parse_film_titles']

from . import parse_film_titles