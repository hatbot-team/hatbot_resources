#!/bin/python3

import random
import re

from hb_res.lang_utils.morphology import *
from hb_res.lang_utils.cognates import are_cognates
from hb_res.resources.resource_registry import resource_by_name
# noinspection PyProtectedMember
from hb_res.resources.definitions import \
    _raw_data, RESULT_RESOURCE_NAME, DUMP_RESOURCE_NAME


GAP_VALUE = '###'
CHANGE_SAMPLE_PERCENTAGE = 5


def read_article(source):
    """
    Reads one article from vocab.
    Fixes misOCR'ed '?' instead of 'ё'
    :param source: vocabulary iterable object
    :return: list of article's lines
    """
    article = []
    while True:
        line = source.readline()
        if not line:
            return None

        if len(line.strip(' \n')) > 0:
            article.append(line.strip().replace('?', 'Ё'))
            break

    while True:
        line = source.readline()

        if len(line.strip(' \n')) == 0:
            break
        article.append(line.strip().replace('?', 'Ё'))

    return article


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


def is_good_title(title):
    if title[-1] == '.':
        return False
    title = title.strip('1234567890-')
    if not title.isalpha() or not title.isupper():
        return False

    for parse in morph.parse(title):
        if parse.tag.POS == 'NOUN' and parse.score > 0.01:
            return True
    return False


def correct_usage(word, entry):
    entry = entry.strip()
    for w in re.split('[\W,:;\(\)]+', entry):
        if are_cognates(w, word, length_threshold=4):
            entry = re.sub(w, GAP_VALUE, entry, flags=re.IGNORECASE)

    abbreviation = ' ' + word[0] + '\.'
    entry = re.sub(abbreviation, GAP_VALUE, entry, flags=re.IGNORECASE)
    return entry


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
            meanings.append(correct_usage(get_title(article), definition))
    else:
        # cut first capital after first dot
        for i in range(text.find('.'), len(text)):
            if text[i].isupper():
                text = text[i:]
                break
        if '||' in text:
            text = text[:text.find('||')]
        meanings.append(correct_usage(get_title(article), text))

    return meanings


def parse_dict(name, out, start_id):
    database = open(name)

    cnt, good, total = 0, 0, 0
    cur_id = start_id
    while True:
        article = read_article(database)
        if article is None:
            break
        cnt += 1
        if cnt % 1000 == 0:
            print('%d articles parsed' % cnt)

        title = get_title(article)
        if not is_good_title(title):
            continue
        meanings = extract_meanings(article)
        title = title.replace('Ё', 'Е').replace('ё', 'е')

        out.add_entry(title + ' ' + str(len(meanings)))

        for definition in meanings:
            out.add_entry(str(cur_id) + '@' + definition)
            cur_id += 1
            total += 1

        good += 1

    print('%d articles parsed, %d articles added, %d definitions' % (cnt, good, total))
    return total


def assemble_dict():
    result = resource_by_name(RESULT_RESOURCE_NAME)

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

    dumped_defs = dict()
    for line in dump:
        if len(line.strip()) == 0:
            continue
        num_exp = int(line.split()[1])
        for i in range(num_exp):
            tokens = dump.__next__().split('@')
            key, text = tokens[0], tokens[1]
            if random.randint(0, 100) < CHANGE_SAMPLE_PERCENTAGE:
                dumped_defs[key] = text

    sanity_result = True

    result = resource_by_name(RESULT_RESOURCE_NAME).entries()
    for line in result:
        num_exp = int(line.split()[1])
        for i in range(num_exp):
            tokens = result.__next__().split('@')
            key, text = tokens[0], tokens[1]
            if key in dumped_defs.keys() and dumped_defs[key] != text:
                print('Id ' + key + ' changed: ')
                print('\tDump: ' + dumped_defs[key])
                print('\tCurr: ' + text)
                sanity_result = False

    return sanity_result


def dump_dict():
    dump = resource_by_name(DUMP_RESOURCE_NAME)
    dump.clear()

    for line in resource_by_name(RESULT_RESOURCE_NAME).entries():
        dump.add_entry(line.strip())


assemble_dict()
if sanity_check():
    dump_dict()
else:
    print('Something changed. Merge manually if needed')
