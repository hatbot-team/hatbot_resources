__author__ = 'ryad0m'

# noinspection PyProtectedMember
from preparation.resources.ngram import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers

ngram_mods = [
    modifiers.check_contains_valid_parts(2, 0.1, '\W+'),
    modifiers.shadow_cognates(5, '\W+', with_question=True),
    modifiers.delete_multiple_gaps(0),
    modifiers.calculate_key()
]

@gen_resource('NgramResource', ngram_mods)
def read_data():
    with open(_raw_data, 'r', encoding='utf-8') as source:
        explanations = dict()
        for line in source:
            word, expl, rate = line.strip('\n').split('\t')
            if explanations.get((word, expl)) is None:
                explanations[(word, expl)] = rate
            else:
                explanations[(word, expl)] += rate
        for (word, expl), rate in sorted(explanations.items()):
            yield Explanation(word, expl, prior_rating=int(rate) / 400000)

