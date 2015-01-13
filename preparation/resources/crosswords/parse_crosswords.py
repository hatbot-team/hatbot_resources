__author__ = 'shkiper'

# noinspection PyProtectedMember
from preparation.resources.crosswords import _raw_data
from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation
from preparation import modifiers

crosswords_mods = [
    modifiers.re_replace('p', 'р'),
    modifiers.strip(target_field='title'),
    modifiers.strip(),
    modifiers.normalize_title(),
    modifiers.re_replace(r'\s+', ' '),
    modifiers.re_replace(r'([,:])(?=[^ ])', '\1 '),
    modifiers.str_replace(r' :', ':'),
    modifiers.str_replace(r' ,', ','),
    modifiers.shadow_cognates(8, '\W+', with_pronoun=True),
    modifiers.remove_to_much_gap_percentage(r'\W+', r'\*(\w+)[?]?\*', 0.5),
    modifiers.calculate_key()
]


@gen_resource('CrosswordsResource', crosswords_mods)
def read_data():
    met = set()
    with open(_raw_data, 'r', encoding='utf-8') as source:
        for line in source:
            tokens = line.split('$')
            word_and_text = tokens[1], tokens[2]
            if word_and_text not in met:
                met.add(word_and_text)
                yield Explanation(*word_and_text)
