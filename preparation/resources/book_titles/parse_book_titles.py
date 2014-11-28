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

@modifiers.modifier_factory
def add_author():
    def apply(e: Explanation):
        ret = copy.copy(e)
        ret.text = ret.text + " Автор: " + e.author
        return ret
    return apply


book_titles_mods = [
    modifiers.check_contains_valid_parts(2, 0.1, '\W+'),
    modifiers.shadow_title_with_question(),
    modifiers.normalize_title(),
    add_common_prefix(),
    add_author(),
    modifiers.shadow_cognates(5, '\W+'),
    modifiers.delete_multiple_gaps(0),
    modifiers.calculate_key()
]

@gen_resource('BookTitlesResource', book_titles_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        count = 0
        while True:
            count += 1
            title = source.readline().strip('\n')
            author = source.readline().strip('\n')
            if not title: break
            for word in re.split('\W+', title):
                if len(word) > 0:
                    explanation = Explanation(title = word, text = title, prior_rating = 1.0/count)
                    explanation.author = author
                    yield explanation
