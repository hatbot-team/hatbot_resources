__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.phraseological import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers
import re

phraseological_mods = [
    modifiers.check_contains_valid_parts(2, 0.1, '\W+'),
    modifiers.shadow_title_with_question(),
    modifiers.normalize_title(),
    modifiers.shadow_cognates(5, '\W+'),
    modifiers.delete_multiple_gaps(0),
    modifiers.re_replace(' ([,!?])', r'\1'),
    modifiers.strip(),
    modifiers.calculate_key()
]


@gen_resource('PhraseologicalResource', phraseological_mods)
def read_data():
    phrases = set()
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            phrases.add(line)
    for line in sorted(phrases):
        for word in sorted(set(re.split('\W+', line))):
            if len(word) > 0:
                yield Explanation(word, line.strip('\n'))
