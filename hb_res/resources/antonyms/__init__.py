from hb_res.resources import FileResource

__author__ = 'Алексей'

__all__ = ['parse_antonyms']

import os
from hb_res.resources.resource_registry import register_resource

RESULT_RESOURCE_NAME = 'antonyms'

PREFIX = os.path.dirname(os.path.abspath(__file__))

INPUT_NAME = PREFIX + '/raw_data/antonyms_raw.txt'
RESULT_NAME = PREFIX + '/output/antonyms.txt'

register_resource(RESULT_RESOURCE_NAME, FileResource(RESULT_NAME))
