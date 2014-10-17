__author__ = 'Алексей'

import os

from resources.resource_registry import register_resource
from resources.FileResource import FileResource

__all__ = ['import_from_site', 'parse_synonyms', 'init_dictionary', 'dump_dictionary']

RESULT_RESOURCE_NAME = 'synonyms'

PREFIX = os.path.dirname(os.path.abspath(__file__))

INPUT_NAME = PREFIX + '/raw_data/synonyms_raw.txt'
RESULT_NAME = PREFIX + '/output/synonyms.txt'

register_resource(RESULT_RESOURCE_NAME, FileResource(RESULT_NAME))

from .raw_data.raw_extracter import import_from_site
from .parse_synonyms import init_dictionary
from .parse_synonyms import dump_dictionary
