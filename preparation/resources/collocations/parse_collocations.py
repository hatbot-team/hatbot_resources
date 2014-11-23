__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.collocations import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers
from preparation.lang_utils.morphology import morph
import copy

@modifiers.modifier_factory
def inflect_first_word():
    def apply(e: Explanation):
        ret = copy.copy(e)
        words = e.text.split(' ')
        parses = [p for p in morph.parse(words[1]) if p.tag.POS == 'NOUN' and p.score > 0.01]
        if len(parses) < 1:
            return e
        second = parses[0].normalized
        first = morph.parse(words[0])[0]
        if sum(p.score for p in morph.parse(words[0]) if p.tag.POS in ['ADJF', 'ADJS', 'COMP', 'PRTF', 'PRTS']) < 0.4:
            return e
        if second.tag.case is None or second.tag.gender is None or second.tag.number is None:
            return e
        first = first.inflect({second.tag.case,
                               second.tag.gender,
                               second.tag.number})
        if first is None:
            return e
        ret.text = ' '.join([first.word, second.word])
        return ret
    return apply

collocations_mods = [
    inflect_first_word(),
    modifiers.check_contains_valid_parts(2, 0.1, '\W+'),
    modifiers.shadow_title_with_question(),
    modifiers.normalize_title(),
    modifiers.shadow_cognates(5, '\W+'),
    modifiers.delete_multiple_gaps(0),
    modifiers.calculate_key()
]

@gen_resource('CollocationsResource', collocations_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            line = ' '.join(line.split()[0:2])
            for word in line.split(' '):
                if len(word) > 0:
                    yield Explanation(word, line)