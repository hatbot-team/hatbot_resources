__author__ = 'skird'

from os import path

__all__ = ['parse_definitions']

PREFIX = path.join(path.dirname(path.abspath(__file__)), 'raw_data')
PART_PREFIX, PART_SUFFIX = 'ozh', '_s.txt'
PARTS = 5

RESULT_RESOURCE_NAME = 'definitions'
DUMP_RESOURCE_NAME = 'definitions_dump'

OUTPUT_PREFIX = path.join(path.dirname(path.abspath(__file__)), 'output')
RESULT_NAME = path.join(OUTPUT_PREFIX, 'ozh_full.txt')
DUMP_NAME = path.join(OUTPUT_PREFIX, 'ozh_dumped.txt')

_raw_data = [path.join(PREFIX, PART_PREFIX + str(i) + PART_SUFFIX) for i in range(1, PARTS + 1)]

from . import parse_definitions

# register_resource(RESULT_RESOURCE_NAME, FileExplanationStorage(RESULT_NAME))
# register_resource(DUMP_RESOURCE_NAME, FileExplanationStorage(DUMP_NAME))
