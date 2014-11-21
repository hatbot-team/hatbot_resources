__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.book_titles import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers
import re
import copy

@modifiers.modifier_factory
def add_common_prefix():
    def apply(e: Explanation):
        ret = copy.copy(e)
        ret.text = "Книга: " + ret.text
        return ret
    return apply

book_titles_mods = [
    modifiers.shadow_cognates(None, '\W+'),
    modifiers.normalize_title(),
    modifiers.shadow_cognates(5, '\W+'),
    modifiers.delete_multiple_gaps(1),
    modifiers.check_contains_valid_parts(1, 0.1, '\W+'),
    add_common_prefix(),
    modifiers.calculate_key()
]

@gen_resource('BookTitlesResource', book_titles_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        cnt = 0
        while True:
            title = source.readline()
            author = source.readline()
            cnt += 1
            if not title: break
            if cnt > 100: break
            for word in re.split('\W+', title):
                if len(word) > 0:
                    yield Explanation(word, title)
