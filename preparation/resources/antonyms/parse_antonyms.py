__author__ = 'Алексей'

# noinspection PyProtectedMember
from preparation.resources.antonyms import _raw_data
from preparation import modifiers
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation

synonyms_mods = [
    modifiers.normalize_title(),
    modifiers.delete_complex_words_explanation('#', ' '),
    modifiers.shadow_cognates(6, '#'),
    modifiers.normalize_words_in_explanation('#'),
    modifiers.change_words_separator('#', ', '),
    modifiers.calculate_key()
]

@gen_resource('AntonymsResource', synonyms_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            [title, text] = line.split('@')
            yield Explanation(title, text)
