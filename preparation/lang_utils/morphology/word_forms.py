import re
from pymorphy2.analyzer import Parse
import functools

from preparation.lang_utils.morphology import morph
from preparation.blacklists import TITLE_BLACKLIST, TITLE_WHITELIST


__author__ = 'moskupols'

_BANNED_TAGS = ('Abbr', 'Name', 'Surn', 'Patr', 'Geox',
                'Orgn', 'Trad', 'Vpre', 'Erro', 'Init')
TYPICAL_RUSSIAN_RE = re.compile(r'^([ёа-я]{2,}|[ёа-я]{2,}-[ёа-я]{2,})$')


def get_initial_forms(form: str, part_filter=None) -> list:
    """
    Gets all possible initial forms (there are several of them sometimes) of a given word.
    Optional argument part_filter allows to prune unnecessary ambiguity with part of speech.

    >>> get_initial_forms('Дядя')
    ['дядя']
    >>> get_initial_forms('самых')
    ['самый']
    >>> get_initial_forms('честных')
    ['честной', 'честный']
    >>> get_initial_forms('правил')
    ['правило', 'править']
    >>> get_initial_forms('правил', 'NOUN')
    ['правило']
    >>> get_initial_forms('правил', ['VERB'])
    ['править']

    :param form: a russian word
    :param part_filter: something that supports `in' operator: str, list, set etc. If it is a container,
    it should contain only Part-of-speech names according to pymorphy2 enumerations
    :return: a list of possible initial forms of the given word in lowercase.
    It's guaranteed that there are no repetitions.
    Variants are generated in the order of descending certainty.
    """
    met = set()
    ret = []
    for p in morph.parse(form):
        if p.score < 0.01:
            continue
        if part_filter is None or p.tag.POS in part_filter:
            norm = p.normal_form
            if norm not in met:
                ret.append(norm)
                met.add(norm)
    return ret


def looks_like_valid_russian(word: str):
    return word in TITLE_WHITELIST \
           or (word not in TITLE_BLACKLIST and TYPICAL_RUSSIAN_RE.match(word))


def _is_valid_noun_parse(parsed: Parse):
    tag = parsed.tag
    if tag.POS != 'NOUN':
        return False
    for ban in _BANNED_TAGS:
        if ban in str(tag):
            return False
    return True


@functools.lru_cache(None)
def get_valid_noun_initial_form(word: str, score_threshold=0.) -> str:
    if not looks_like_valid_russian(word.lower()):
        return None
    possible_forms = [p for p in morph.parse(word) if looks_like_valid_russian(p.normal_form)]
    possible_forms = [p for p in possible_forms if _is_valid_noun_parse(p) and p.score >= score_threshold]
    if len(possible_forms) == 0:
        return None
    else:
        return max(possible_forms, key=lambda x: (x.score, x.word)).normal_form
