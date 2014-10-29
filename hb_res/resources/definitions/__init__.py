from hb_res.resources.FileExplanationStorage import FileExplanationStorage

__author__ = 'skird'

import os

from hb_res.resources.resource_registry import register_resource


__all__ = ['parse_definitions']

PREFIX = os.path.dirname(os.path.abspath(__file__)) + '/raw_data/'
PART_PREFIX, PART_SUFFIX = 'ozh', '_s.txt'
PARTS = 5

RESULT_RESOURCE_NAME = 'definitions'
DUMP_RESOURCE_NAME = 'definitions_dump'

OUTPUT_PREFIX = os.path.dirname(os.path.abspath(__file__)) + '/output/'
RESULT_NAME = OUTPUT_PREFIX + 'ozh_full.txt'
DUMP_NAME = OUTPUT_PREFIX + 'ozh_dumped.txt'

_raw_data = [PREFIX + PART_PREFIX + str(i) + PART_SUFFIX for i in range(1, PARTS + 1)]

register_resource(RESULT_RESOURCE_NAME, FileExplanationStorage(RESULT_NAME))
register_resource(DUMP_RESOURCE_NAME, FileExplanationStorage(DUMP_NAME))
