__author__ = 'Алексей'

from resources.synonyms import init_dictionary
from resources.synonyms import dump_dictionary
from resources.resource_registry import resource_by_name

# noinspection PyProtectedMember
from resources.antonyms import \
    INPUT_NAME, RESULT_RESOURCE_NAME

THRESHOLD = 6

antonyms = dict()
init_dictionary(INPUT_NAME, antonyms, THRESHOLD)
dump_dictionary(resource_by_name(RESULT_RESOURCE_NAME), antonyms)