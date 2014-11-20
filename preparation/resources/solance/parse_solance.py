__author__ = 'pershik'

from preparation.resources.solance import _raw_data
from preparation import modifiers
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation

solance_mods = [
    modifiers.normalize_title(),

    modifiers.re_replace('[^#]+? [^#]+?(#|$)', ''),  # remove multi-word explanations (containing spaces)
    modifiers.re_fullmatch_ban(''),

    modifiers.delete_cognates(4, '\n'),
    modifiers.delete_not_initial_form(),
    #modifiers.choose_normal_words_in_explanation('#'),
    modifiers.calculate_key()
]


@gen_resource('SolanceResource', solance_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            [title, buf] = line.split('@')
            entries = buf.split('#')
            for entry in entries:
                if not entry.strip():
                    continue
                [text, rating] = entry.split('&')
                yield Explanation(title, text, prior_rating=rating)