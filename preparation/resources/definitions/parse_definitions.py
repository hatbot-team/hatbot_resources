#!/bin/python3

# import random
import copy
import re

from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation

# noinspection PyProtectedMember
from preparation.resources.definitions import _raw_data
from preparation import modifiers


# CHANGE_SAMPLE_PERCENTAGE = 5

@modifiers.modifier_factory
def shadow_abbreviations():
    def apply(e: Explanation):
        ret = copy.copy(e)
        abbreviation = ' ' + e.title[0] + '\.'
        ret.text = re.sub(abbreviation, modifiers.GAP_VALUE, ret.text, flags=re.IGNORECASE)
        return ret
    return apply

definitions_mods = [
    modifiers.re_fullmatch_ban('.*\\.', target_field='title'),
    modifiers.strip('1234567890-', target_field='title'),
    modifiers.re_fullmatch_ban('(?!([А-Я]+))', target_field='title'),
    modifiers.re_replace('Ё', 'Е', target_field='title'),
    modifiers.normalize_title(),

    modifiers.strip(),
#    modifiers.re_replace('\\?', 'ё'),  # Fixes misOCR'ed '?' instead of 'ё'
    modifiers.shadow_cognates(4, '[\W,:;\(\)]+'),
    shadow_abbreviations(),

    modifiers.calculate_key()
]


@gen_resource('DefinitionsResource', modifiers=definitions_mods)
def read_articles():
    """
    Generator which yields raw Explanations based on definitions dict
    """
    with open(_raw_data, 'r', encoding='utf-8') as source:
        while True:
            title = source.readline().strip('\n')
            if not title: break
            desc = source.readline().strip('\n')
            yield Explanation(title, desc)
# def sanity_check():
#     random.seed = 314
#     try:
#         dump = resource_by_name(DUMP_RESOURCE_NAME).entries()
#     except FileNotFoundError:
#         print('Dump doesn\'t exist. It will be created')
#         return True
#
#     dumped_definitions = dict()
#     for explanation in dump:
#         if random.randint(0, 100) < CHANGE_SAMPLE_PERCENTAGE:
#             dumped_definitions[explanation.key] = explanation.text
#
#     sanity_result = True
#
#     result = resource_by_name(RESULT_RESOURCE_NAME).entries()
#     for explanation in result:
#         key, text = explanation.key, explanation.text
#         if key in dumped_definitions.keys() and dumped_definitions[key] != text:
#             print('Id ' + key + ' changed: ')
#             print('\tDump: ' + dumped_definitions[key])
#             print('\tCurr: ' + text)
#             sanity_result = False
#
#     return sanity_result


# def dump_dict():
#     dump = resource_by_name(DUMP_RESOURCE_NAME)
#     dump.clear()
#
#     for explanation in resource_by_name(RESULT_RESOURCE_NAME).entries():
#         dump.add_entry(explanation)
#
#
# assemble_dict()
# if sanity_check():
#     dump_dict()
# else:
#     print('Something changed. Merge manually if needed')
