import itertools

from preparation.resources.Resource import gen_resource
from preparation import modifiers
from hb_res.explanations.Explanation import Explanation


sample_modifiers = (
    modifiers.str_replace('?', 'ё'),
    modifiers.shadow_cognates(length_threshold=3, sep_re='(\\s|!|\\.)+'),
    modifiers.re_replace('\\.', ' '),
    modifiers.normalize_title(),
    modifiers.calculate_key(),
)


@gen_resource('SampleResource', sample_modifiers)
def sample_parser():
    raw_expls = itertools.starmap(Explanation, (
        ('ПОРА', 'Однажды.в.студ?ную.зимнюю.пору.я.из.лесу.вышел.'),
        ('ИВАН', 'Один день Ивана Денисовича'),
        ('унылая', 'Унылая пора! очей очарованье!')
    ))
    return raw_expls
