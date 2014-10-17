__author__ = 'Алексей'


import codecs
from sys import stderr
from lang_utils.cognates import are_cognates
from lang_utils.morphology import get_valid_noun_initial_form
from resources.resource_registry import resource_by_name

# noinspection PyProtectedMember
from resources.synonyms import \
    INPUT_NAME, RESULT_RESOURCE_NAME

THRESHOLD = 4


def init_dictionary(input_name, res_dict, threshold):
    try:
        file = codecs.open(input_name, 'r', encoding='utf-8')
    except FileNotFoundError:
        stderr.write('No raw dictionary\n')
        return
    for line in file:
        [new_initial, explain_list] = line.split('@')
        if new_initial == get_valid_noun_initial_form(new_initial):
            new_list = [w for w in explain_list.split('#')
                        if not are_cognates(new_initial, w, threshold)
                        and get_valid_noun_initial_form(w) is not None
                        and len(w.split(' ')) == 1]
            if len(new_list) != 0:
                if new_initial in res_dict.keys():
                    res_dict[new_initial].extend(new_list)
                else:
                    res_dict[new_initial] = new_list


def dump_dictionary(resource, res_dict):
    resource.clear()

    for word in res_dict.keys():
        line = word + "  "
        for syn in res_dict[word]:
            line = line + syn + " "
        resource.add_entry(line)


synonyms_dict = dict()
init_dictionary(INPUT_NAME, synonyms_dict, THRESHOLD)
dump_dictionary(resource_by_name(RESULT_RESOURCE_NAME), synonyms_dict)