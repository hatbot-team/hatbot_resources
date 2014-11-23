from hb_res.storage import get_storage

__author__ = 'pershik'

from preparation.resources.solance import _raw_data
from preparation import modifiers
from preparation.resources.Resource import gen_resource, names_registered
from hb_res.explanations import Explanation

solance_mods = [
    modifiers.delete_not_initial_form_title(),

    modifiers.re_fullmatch_ban(''),

    modifiers.delete_cognates(4, '\n'),
    modifiers.delete_low_rating(50),
    modifiers.calculate_key()
]

explanations = dict()


def get_resource_explanations(resource_name):
    resource_name = resource_name.replace('Resource', '')
    storage = get_storage(resource_name)
    for explanation in storage.entries():
        if explanation is None:
            continue
        if not explanations.__contains__(explanation.title):
            explanations[explanation.title] = list()
        explanations[explanation.title].append(explanation.text)


def get_all_explanations():
    for resource_name in names_registered():
        print(resource_name + " is reading")
        print(len(explanations))
        if resource_name != 'SolanceResource':
            get_resource_explanations(resource_name)


@gen_resource('SolanceResource', solance_mods)
def read_data():
    get_all_explanations()
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            [title, buf] = line.split('@')
            entries = buf.split('#')
            for entry in entries:
                if not entry.strip():
                    continue
                [text, rating] = entry.split('&')
                if title == text:
                    continue
                if not explanations.__contains__(text):
                    continue
                for explanation in explanations[text]:
                    full_text = explanation + ". Созвучие к этому слову"
                    yield Explanation(title, full_text, prior_rating=float(rating))