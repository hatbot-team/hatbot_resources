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
    modifiers.re_replace('\\?', 'ё'),  # Fixes misOCR'ed '?' instead of 'ё'
    modifiers.shadow_cognates(4, '[\W,:;\(\)]+'),
    shadow_abbreviations(),

    modifiers.calculate_key()
]


@gen_resource('DefinitionsResource', modifiers=definitions_mods)
def read_articles():
    """
    Generator which yields raw Explanations based on definitions dict
    """

    def get_title(article_lines):
        """
        Parse article text to get its title
        :param article_lines: list of article's lines
        :return:
        """
        name = article_lines[0].split()[0]
        if '[' in name[0]:
            name = name[:name.find('[')]
        return name.strip(',:1234567890')

    def extract_meanings(article_lines):
        text = ' '.join(article_lines)
        if '1.' in text:
            # parse numbered definitions
            borders = []
            for i in range(1, 10):
                current = chr(i + 48) + '.'
                if current in text:
                    borders.append(text.find(current))
            for i in range(len(borders)):
                next_occ = borders[i + 1] if i + 1 < len(borders) else len(text)
                definition = text[borders[i] + 2:next_occ]
                if '||' in definition:
                    definition = definition[:definition.find('||')]
                yield definition
        else:
            # cut first capital after first dot
            for i in range(text.find('.'), len(text)):
                if text[i].isupper():
                    text = text[i:]
                    break
            if '||' in text:
                text = text[:text.find('||')]
            yield text

    # read file and call title and meanings getters
    for part_path in _raw_data:
        print('Parsing ' + part_path + '...')
        with open(part_path) as source:
            while True:
                line = source.readline()
                if line is None:
                    raise StopIteration
                line = line.strip(' \n')
                if len(line) > 0:
                    article = [line]
                    while True:
                        line = source.readline().strip(' \n')
                        if len(line) == 0:
                            break
                        article.append(line)
                    title = get_title(article)
                    for meaning in extract_meanings(article):
                        yield Explanation(title, meaning)


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
