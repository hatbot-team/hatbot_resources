#!/bin/python3

import random
import re

from preparation.lang_utils.morphology import morph
from hb_res.lang_utils.cognates import are_cognates
from hb_res.resources.resource_registry import resource_by_name



# noinspection PyProtectedMember
from preparation.resources.definitions import \
    _raw_data, RESULT_RESOURCE_NAME, DUMP_RESOURCE_NAME

from hb_res.explanations import Explanation
from hb_res.explanations import ExplanationKey


GAP_VALUE = '###'
CHANGE_SAMPLE_PERCENTAGE = 5


def get_title(article):
    """
    Parse article text to get its title
    :param article: list of article's lines
    :return:
    """
    name = article[0].split()[0]
    for i in range(len(name)):
        if article[0][i] == '[':
            name = name[0:i]
            break
    return name.strip(',:1234567890')


def extract_meanings(article):
    text = ' '.join(article)
    meanings = list()
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
            meanings.append(definition)
    else:
        # cut first capital after first dot
        for i in range(text.find('.'), len(text)):
            if text[i].isupper():
                text = text[i:]
                break
        if '||' in text:
            text = text[:text.find('||')]
        meanings.append(text)

    return meanings


def read_articles(source) -> Explanation:
    """
    Generator which yields raw Explanations
    :param source: vocabulary iterable object
    :return: list of article's lines
    """
    while True:
        line = source.readline()
        if not line:
            raise StopIteration

        if len(line.strip(' \n')) > 0:
            article = [line.strip(' \n')]
            while True:
                line = source.readline()

                if len(line.strip(' \n')) == 0:
                    break
                article.append(line.strip(' \n'))
            title = get_title(article)
            meanings = extract_meanings(article)
            for meaning in meanings:
                yield Explanation(title, meaning)


def fix_misreads(explanation: Explanation) -> Explanation:
    """
    Fixes misOCR'ed '?' instead of 'ё'
    """
    new_text = explanation.text.strip().replace('?', 'ё')
    return Explanation(explanation.title, new_text, None, explanation.prior_rating)


def correct_usage(explanation: Explanation) -> Explanation:
    new_text = explanation.text.strip()
    for w in re.split('[\W,:;\(\)]+', new_text):
        if are_cognates(w, explanation.title, length_threshold=4):
            new_text = re.sub(w, GAP_VALUE, new_text, flags=re.IGNORECASE)

    abbreviation = ' ' + explanation.title[0] + '\.'
    new_text = re.sub(abbreviation, GAP_VALUE, new_text, flags=re.IGNORECASE)
    return Explanation(explanation.title, new_text, None, explanation.prior_rating)


def correct_title(explanation: Explanation) -> Explanation:
    if explanation.title[-1] == '.':
        return None
    new_title = explanation.title.strip('1234567890-')
    if not new_title.isalpha() or not new_title.isupper():
        return None
    new_title = new_title.replace('Ё', 'Е').replace('ё', 'е')

    for parse in morph.parse(new_title):
        if parse.tag.POS == 'NOUN' and parse.score > 0.01:
            return Explanation(new_title, explanation.text, None, explanation.prior_rating)
    return None


def calculate_key(explanation: Explanation) -> Explanation:
    if explanation.key is not None:
        return explanation

    new_key = ExplanationKey.for_text(explanation.text)
    return Explanation(explanation.title, explanation.text, new_key, explanation.prior_rating)


def parse_dict(name, out, start_id):
    modifiers = [fix_misreads, correct_title, correct_usage, calculate_key]
    database = open(name)

    cnt, total = 0, 0
    cur_id = start_id
    for explanation in read_articles(database):
        cnt += 1

        if cnt % 1000 == 0:
            print('%d articles parsed' % cnt)

        for modifier in modifiers:
            if explanation is not None:
                explanation = modifier(explanation)

        if explanation is not None:
            assert(explanation.key is not None)
            out.add_entry(explanation)
            cur_id += 1
            total += 1

    print('%d articles parsed, %d definitions' % (cnt, total))
    return total


def assemble_dict():
    result = resource_by_name(RESULT_RESOURCE_NAME)
    result.clear()

    cur_id = 0
    for part in _raw_data:
        print('Parsing ' + part + '...')
        cur_id += parse_dict(part, result, cur_id)


def sanity_check():
    random.seed = 314
    try:
        dump = resource_by_name(DUMP_RESOURCE_NAME).entries()
    except FileNotFoundError:
        print('Dump doesn\'t exist. It will be created')
        return True

    dumped_definitions = dict()
    for explanation in dump:
        if random.randint(0, 100) < CHANGE_SAMPLE_PERCENTAGE:
            dumped_definitions[explanation.key] = explanation.text

    sanity_result = True

    result = resource_by_name(RESULT_RESOURCE_NAME).entries()
    for explanation in result:
        key, text = explanation.key, explanation.text
        if key in dumped_definitions.keys() and dumped_definitions[key] != text:
            print('Id ' + key + ' changed: ')
            print('\tDump: ' + dumped_definitions[key])
            print('\tCurr: ' + text)
            sanity_result = False

    return sanity_result


def dump_dict():
    dump = resource_by_name(DUMP_RESOURCE_NAME)
    dump.clear()

    for explanation in resource_by_name(RESULT_RESOURCE_NAME).entries():
        dump.add_entry(explanation)


assemble_dict()
if sanity_check():
    dump_dict()
else:
    print('Something changed. Merge manually if needed')
