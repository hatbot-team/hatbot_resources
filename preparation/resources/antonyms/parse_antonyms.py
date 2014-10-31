__author__ = 'Алексей'

from preparation.resources.synonyms import init_dictionary
from preparation.resources.synonyms import dump_dictionary
from preparation.resources.resource_registry import resource_by_name
from preparation.resources.antonyms import INPUT_NAME, RESULT_RESOURCE_NAME

THRESHOLD = 6

antonyms = dict()
init_dictionary(INPUT_NAME, antonyms, THRESHOLD)
dump_dictionary(resource_by_name(RESULT_RESOURCE_NAME), antonyms)
