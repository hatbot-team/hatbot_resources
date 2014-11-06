__author__ = 'Алексей'

# noinspection PyProtectedMember
from preparation.resources.antonyms import _raw_data
from preparation import modifiers
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
import copy

@modifiers.modifier_factory
def add_antonyms_common_text():
    def apply(e: Explanation):
        if e.text.find(',') == -1:
            text = "антоним к слову " + e.text
        else:
            text = "антоним к словам" + e.text
        return Explanation(copy.copy(e.title), text)
    return apply

antonyms_mods = [
    modifiers.normalize_title(),
    modifiers.delete_complex_words_explanation('#', ' '),
    modifiers.shadow_cognates(6, '#'),
    modifiers.normalize_words_in_explanation('#'),
    modifiers.change_words_separator('#', ', '),
    add_antonyms_common_text(),
    modifiers.calculate_key()
]

@gen_resource('AntonymsResource', antonyms_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            [title, text] = line.split('@')
            yield Explanation(title, text)
