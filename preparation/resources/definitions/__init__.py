__author__ = 'skird'

from os import path

__all__ = ['parse_definitions']

RAW_DIR = path.join(path.dirname(path.abspath(__file__)), 'raw_data')
PART_FORMAT = 'ozh{}_s.txt'
PARTS = 5

_raw_data = [path.join(RAW_DIR, PART_FORMAT.format(i)) for i in range(1, PARTS + 1)]

from . import parse_definitions
