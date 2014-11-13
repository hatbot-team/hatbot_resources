__author__ = 'Алексей'

import copy
# noinspection PyProtectedMember
from preparation.resources.antonyms import _raw_data
from preparation import modifiers
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation


@modifiers.modifier_factory
def add_antonyms_common_text():
    def apply(e: Explanation):
        if e.text.find(',') == -1:
            text = "антоним к слову " + e.text
        else:
            text = "антоним к словам " + e.text
        ret = copy.copy(e)
        ret.text = text
        return ret
    return apply

antonyms_mods = [
    modifiers.normalize_title(),

    modifiers.re_replace('[^#]+ [^#]+(#|$)', ''),  # remove multi-word antonyms (containing spaces)
    modifiers.re_fullmatch_ban(''),

    modifiers.delete_cognates(6, '#'),
    modifiers.choose_normal_words_in_explanation('#'),
    modifiers.re_replace('#', ', ', target_field='text'),
    add_antonyms_common_text(),
    modifiers.calculate_key()
]


@gen_resource('AntonymsResource', antonyms_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            [title, text] = line.split('@')
            yield Explanation(title, text)
