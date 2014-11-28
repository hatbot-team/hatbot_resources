__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.film_titles import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers
import re
import copy

@modifiers.modifier_factory
def add_common_prefix():
    def apply(e: Explanation):
        ret = copy.copy(e)
        ret.text = "Фильм: " + ret.text
        return ret
    return apply

film_titles_mods = [
    modifiers.check_contains_valid_parts(2, 0.1, '\W+'),
    modifiers.shadow_title_with_question(),
    modifiers.normalize_title(),
    modifiers.shadow_cognates(5, '\W+'),
    modifiers.delete_multiple_gaps(0),
    add_common_prefix(),
    modifiers.calculate_key()
]

@gen_resource('FilmTitlesResource', film_titles_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        max_count = 0
        while True:
            title = source.readline().strip('\n')
            if not title: break
            count = int(source.readline().strip('\n'))
            max_count = max(max_count, count)
            for word in re.split('\W+', title):
                if len(word) > 0:
                    yield Explanation(title = word, text = title, prior_rating = float(count)/max_count)
