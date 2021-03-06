__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.collocations import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers

collocations_mods = [
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