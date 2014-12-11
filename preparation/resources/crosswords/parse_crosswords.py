__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.crosswords import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers

crosswords_mods = [
    modifiers.strip('.'),
    modifiers.normalize_title(),
    modifiers.calculate_key()
]

@gen_resource('CrosswordsResource', crosswords_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            tokens = line.split('$')
            word, text = tokens[1], tokens[2]
            yield Explanation(word.strip().lower(), text.strip())
