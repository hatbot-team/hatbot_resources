__author__ = 'shkiper'

from preparation.lang_utils.frequency import get_frequent_number, get_average_frequency
from preparation import modifiers
from hb_res.explanations import Explanation
import copy


def choose_best_synonyms_from_list(synonyms_list: list, max_number: int):
    new_synonyms_list = synonyms_list.copy()
    new_synonyms_list.sort(key=get_frequent_number)
    return new_synonyms_list[0:max_number]


@modifiers.modifier_factory
def choose_best_synonyms(max_number: int, separator: str):
    def apply(e: Explanation):
        ret = copy.copy(e)
        best = choose_best_synonyms_from_list(ret.text.split(separator), max_number)
        ret.text = separator.join(best)
        return ret
    return apply


@modifiers.modifier_factory
def calculate_prior_rating(separator: str):
    def apply(e: Explanation):
        frequents = list(map(get_average_frequency, e.text.split(separator)))
        title_frequent = get_average_frequency(e.title)
        e.prior_rating = sum(frequents) / len(frequents) + title_frequent
        return e
    return apply