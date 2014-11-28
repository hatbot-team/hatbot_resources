__author__ = 'shkiper'

from . import morph


def get_best_parse(word: str, part: str):
    possibilities = [x for x in morph.parse(word) if x.tag.POS == part]
    if len(possibilities) == 0:
        return None
    else:
        return max(possibilities, key=lambda x: x.score)

WHO_PARSE = get_best_parse('кто', "NPRO")
WHAT_PARSE = get_best_parse('что', "NPRO")
HE_PARSE = get_best_parse('он', "NPRO")
SHE_PARSE = get_best_parse('она', "NPRO")
IT_PARSE = get_best_parse('оно', "NPRO")
THEY_PARSE = get_best_parse('они', "NPRO")


def replace_noun_with_question(word: str, default: str=None):
    """
    Gets noun and returns a string with this case question for this noun.
    If word is not noun or don't have some morphological characteristics to get it,
    default value will be returned.
    >>> replace_noun_with_question('говорить', '*пропуск*')
    '*пропуск*'
    >>> replace_noun_with_question('проводами')
    'чем?'
    >>> replace_noun_with_question('проводницами')
    'кем?'
    >>> replace_noun_with_question('железы')
    'чего?'
    :param word: word for case question
    :param default: value, which returned if it's unable to get case question
    :return: case question with '?' symbol at the end.
    """
    noun_parse = get_best_parse(word, "NOUN")
    if noun_parse is None:
        return default
    if noun_parse.tag.case is None:
        return default
    if noun_parse.tag.animacy == "anim":
        return WHO_PARSE.inflect({noun_parse.tag.case}).word + '?'
    else:
        return WHAT_PARSE.inflect({noun_parse.tag.case}).word + '?'


def replace_noun_with_pronoun(word: str, default: str=None):
    """
    Replaces noun with noun-pronoun.
    If word is not noun or don't have some morphological characteristics to get it,
    default value will be returned.
    >>> replace_noun_with_pronoun('проводнику')
    'ему'
    >>> replace_noun_with_pronoun('проводнице')
    'ей'
    >>> replace_noun_with_pronoun('проводникам')
    'им'
    >>> replace_noun_with_pronoun('красивый', '*пропуск*')
    '*пропуск*'
    :param word: word for noun to replace
    :param default: value, which returned if it's unable to get pronoun
    :return: noun-pronoun
    """
    noun_parse = get_best_parse(word, "NOUN")
    if noun_parse is None:
        return default
    if noun_parse.tag.case is None:
        return default
    case = noun_parse.tag.case
    gender = noun_parse.tag.gender
    number = noun_parse.tag.number
    if number == 'plur':
        return THEY_PARSE.inflect({case}).word
    if gender == 'neut':
        return IT_PARSE.inflect({case}).word
    if gender == 'femn':
        return SHE_PARSE.inflect({case}).word
    if gender == 'masc':
        return HE_PARSE.inflect({case}).word
    return default