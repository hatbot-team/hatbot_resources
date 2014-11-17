__author__ = 'Алексей'

# noinspection PyProtectedMember
from preparation.resources.synonyms import _raw_data
from preparation import modifiers
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation

synonyms_mods = [
    modifiers.normalize_title(),

    modifiers.re_replace('[^#]+? [^#]+?(#|$)', ''),  # remove multi-word synonyms (containing spaces)
    modifiers.re_fullmatch_ban(''),

    modifiers.delete_cognates(4, '#'),
    modifiers.choose_normal_words_in_explanation('#'),
    modifiers.re_replace('#', ', '),
    modifiers.calculate_key()
]


@gen_resource('SynonymsResource', synonyms_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            [title, text] = line.split('@')
            yield Explanation(title, text)
