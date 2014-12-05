#!/bin/python3

# import random
import copy
import re

from preparation.resources.Resource import gen_resource
from hb_res.explanations import Explanation

# noinspection PyProtectedMember
from preparation.resources.definitions import _raw_data
from preparation import modifiers
from preparation.lang_utils.morphology import replace_noun_with_question


# CHANGE_SAMPLE_PERCENTAGE = 5

@modifiers.modifier_factory
def shadow_abbreviations():
    def apply(e: Explanation):
        ret = copy.copy(e)
        abbreviation_re = r'(?<= ){init}\.'.format(init=e.title[0])
        gap = '*' + replace_noun_with_question(e.title, modifiers.GAP_VALUE.strip('*')) + '*'
        ret.text = re.sub(abbreviation_re, gap, ret.text, flags=re.IGNORECASE)
        return ret
    return apply

definitions_mods = [

    # there is even a board on trello for almost all of these modifiers: trello.com/b/IEP8jusD
    modifiers.strip(' -3', target_field='title'),
    modifiers.translate(
        '?і3',  # the second symbol is not i but \xd1\x96 in utf8
        'ЁЁЗ',
        '",.+:124567890',
        target_field='title'
    ),
    modifiers.str_replace('||', 'П', target_field='title'),
    modifiers.re_search_ban(r'[^-ЁёА-Яа-я]', target_field='title'),
    modifiers.normalize_title(),
    # Text OCR problems

    # modifiers.translate(
    #     '?~[]{}',
    #     'ё-()()',
    #     '|*o'  # the o is latin
    # ),
    # modifiers.re_replace(r'знай\.', 'знач.'),
    # modifiers.str_replace('3а', 'За'),
    # modifiers.re_replace(r'(?<={alph})\d+(-\d+)?'.format(alph=modifiers.ALPH_RE), ''),
    # modifiers.re_replace(r'\s+(?=[,.!?])', ''),

    # Text quality heuristics

    modifiers.re_replace(r'\s+', ' '),

    modifiers.re_replace(r' *[вк]о? *(\d|I)+( *, *(\d|I)+)*( *и *(\d|I)+)? *знач[,.]?', '', re.IGNORECASE),

    modifiers.re_replace(r' *см\. *\S+((, ?| и )\S+)*', ''),

    modifiers.re_replace(r'N(\d+)/(\d+)', ''),
    modifiers.re_replace(r'N\d+', ''),

    modifiers.re_replace('<=', ''),

    modifiers.str_contains_ban('Первая часть сложных'),
    modifiers.str_contains_ban('Образует'),
    modifiers.re_replace('[Сс]окращение:( ([Ёёа-яА-Я;]-?|\(.*\))+)+(\.|, а также| -) *', ''),
    modifiers.re_replace('^\([-Ёёа-яА-Я]+\)', ''),

    modifiers.re_replace(r' -(?={alph}{6,}\b)'.replace('{alph}', modifiers.ALPH_RE), '-'),
    modifiers.re_replace(r'[^*Ёёа-яА-Я]-{alph}+\)?\b'.replace('{alph}', modifiers.ALPH_RE), ''),

    modifiers.re_replace(r'[,:] *(?=[,.:!?)])', ''),
    modifiers.re_replace(r'[.!?] *(?=[.!?])', ''),
    modifiers.re_replace(r' *\( *\)', ''),

    modifiers.re_fullmatch_ban(r'^{notalph}*относящийся\s+к.*'.format(notalph=modifiers.NOTALPH_RE), re.IGNORECASE),

    # https://trello.com/c/bPUl4kqT
    modifiers.re_replace(r'(\bк-р|(?<=не)к-р)', 'котор'),
    # https://trello.com/c/LpoSvAHt
    modifiers.str_replace(r'-н.', '-нибудь'),
    modifiers.str_replace(r'-н,', '-нибудь'),

    modifiers.shadow_cognates(4, modifiers.NOTALPH_RE + '+', with_pronoun=True),

    shadow_abbreviations(),



    # some spaces again, just to make sure

    modifiers.re_replace(r'\s+', ' '),
    modifiers.re_replace(r'\s+(?=[,.!?])', ''),

    modifiers.strip(),
    modifiers.re_replace('^[^*ЁёА-Яа-я]+', ''),

    modifiers.re_fullmatch_ban(''),

    modifiers.remove_to_much_gap_percentage(r'\W+', r'\*(\w+)[?]?\*', 0.5),

    modifiers.calculate_key()
]


@gen_resource('DefinitionsResource', modifiers=definitions_mods)
def read_articles():
    """
    Generator which yields raw Explanations based on definitions dict
    """
    with open(_raw_data, 'r', encoding='utf-8') as source:
        while True:
            title = source.readline().strip('\n')
            if not title: break
            desc = source.readline().strip('\n')
            yield Explanation(title, desc)