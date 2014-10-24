__author__ = 'Алексей'

import os

from hb_res.resources.resource_registry import register_resource
from hb_res.resources.FileExplanationStorage import FileExplanationStorage


__all__ = ['import_from_site', 'parse_synonyms', 'init_dictionary', 'dump_dictionary']

RESULT_RESOURCE_NAME = 'synonyms'

PREFIX = os.path.dirname(os.path.abspath(__file__))

INPUT_NAME = PREFIX + '/raw_data/synonyms_raw.txt'
RESULT_NAME = PREFIX + '/output/synonyms.txt'

register_resource(RESULT_RESOURCE_NAME, FileExplanationStorage(RESULT_NAME))

