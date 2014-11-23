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