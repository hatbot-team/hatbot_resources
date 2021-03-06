"""
 Common modifiers factories for use in resources.

 Although modifier concept is defined as a callable (Explanation)->Explanation,
 different resources may need to tweak its behavior more or less.

 So, most modifiers here are parametrised and all modifiers are supposed
 to be created by their factory functions.

 But for debugging convenience it could be nice to have an informative
 representation of parametrized modifier, not just its family.
 For this purpose every modifier is a subclass of Modifier class,
 which remembers parameters it was constructed with in his repr.

 For factory writing convenience there are two decorators:
 - modifier_factory, which just wraps your factory with Modifier.__init__ call;
 - title_text_modifier_factory is for modifiers such as re_replace, which can
   equally successful work with explanations title or text.
   So, the factory should just produce functions str->str, the decorator will
   use them properly.
   By default produced modifiers affect Explanation.text, but it can be changed
   by passing target_field='title' keyword parameter to the factory.
"""

import itertools
import re
import copy

from hb_res.explanations import Explanation, ExplanationKey
from preparation.lang_utils.cognates import are_cognates
from preparation.lang_utils.morphology import get_valid_noun_initial_form
from preparation.lang_utils.morphology import is_remarkable
from preparation.lang_utils.morphology import replace_noun_with_pronoun, replace_noun_with_question
from preparation.lang_utils.frequency import get_average_frequency
from preparation.lang_utils.morphology.word_forms import looks_like_valid_russian

GAP_VALUE = '*пропуск*'

ALPH_RE = '[ЁёА-Яа-я]'
NOTALPH_RE = '[^ЁёА-Яа-я]'
WORD_RE = ALPH_RE + '+'


class Modifier:
    def __init__(self, *args, _name=None, **kwargs):
        if _name is None:
            _name = self.__name__
        self.__str = '{}({})'.format(
            _name,
            ', '.join(itertools.chain(
                map(repr, args),
                itertools.starmap('{}={!r}'.format, kwargs.items())
            ))
        )

    def __str__(self):
        return self.__str

    def __repr__(self):
        return '<Modifier ' + self.__str + '>'

    def __call__(self, e: Explanation):
        raise NotImplementedError


def modifier_factory(factory, name=None) -> Modifier:
    """
    Wraps modifier factory's products in Modifier subclass, remembering parameters the modifier was parametrized.

    :param factory:
    :param name: factory's name
    :return: Modifier
    """
    if name is None:
        name = factory.__name__

    class DecoratedModifier(Modifier):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, _name=name, **kwargs)
            self._mod = factory(*args, **kwargs)

        def __call__(self, e):
            return self._mod(e)

    return DecoratedModifier


def title_text_modifier_factory(factory, name=None) -> Modifier:
    """
    Adds target_field kwarg to modifier factory, allowing modification either 'title' or 'text' fields.

    :param factory:
    :param name:
    :return: Modifier
    """

    def decorator(*args, target_field='text', **kwargs):
        assert target_field in {'text', 'title'}

        mod = factory(*args, **kwargs)

        def apply(explanation):
            ret = copy.copy(explanation)
            setattr(ret, target_field, mod(getattr(ret, target_field)))
            if getattr(ret, target_field) is None:
                ret = None
            return ret

        return apply

    if name is None:
        name = factory.__name__

    return modifier_factory(decorator, name)


@title_text_modifier_factory
def strip(chars: str=None):
    """
    Constructs modifier that calls `str.strip` on field specified in `target_field` kwarg.

    `target_field` is a kwarg that defaults to 'text'.

    :param chars: same as for str.strip
    :return Modifier
    """
    return lambda s: s.strip(chars)


@title_text_modifier_factory
def str_replace(pattern: str, replacement: str, count: int=-1):
    """
    Constructs modifier that replaces e.`target_field` with e.`target_field`.replace(pattern, replacement, count)
    (for given Explanation e).

    `target_field` is a kwarg that defaults to 'text'.

    :param pattern: pattern to replace
    :param replacement: replacement
    :param count: number of times to perform replacement
    :return Modifier
    """
    return lambda s: s.replace(pattern, replacement, count)


@title_text_modifier_factory
def translate(*args):
    """
    Constructs a modifier that applies str.translate(e.`target_field`, str.maketrans(*args))
    on given explanation e.

    :return: Modifier
    """
    trans = str.maketrans(*args)
    return lambda s: s.translate(trans)


@title_text_modifier_factory
def str_contains_ban(substr):
    """
    Constructs a modifier that bans explanations whose e.`target_field` contains substr as a substring.

    :param substr: substring to seek
    :return: Modifier
    """
    return lambda s: s if substr not in s else None


@title_text_modifier_factory
def re_replace(pattern, replacement: str, flags: int=0):
    """
    Constructs modifier that replaces e.`target_field`
    with re.sub(pattern, replacement, e.`target_field`, flags=flags)
    (for given Explanation e).

    `target_field` is a kwarg that defaults to 'text'.

    :param pattern: str or compiled regexp to replace
    :param replacement: replacement
    :param flags: re compilation flags
    :return Modifier
    """
    if isinstance(pattern, (str, bytes)):
        pattern = re.compile(pattern, flags)
    return lambda s: pattern.sub(replacement, s)


@title_text_modifier_factory
def re_fullmatch_ban(pattern, flags: int=0):
    """
    Constructs modifier that bans explanations whose `target_field` matches exactly to `pattern` regexp.

    target_field is a kwarg that defaults to 'text'.

    :param pattern: regexp
    :param flags: re construction flags
    :return Modifier
    """
    # we emulate re.fullmatch behaviour by adding '^' and '$' to the pattern
    assert isinstance(pattern, (str, bytes))
    if isinstance(pattern, bytes):
        pattern = b'^' + pattern + b'$'
    else:
        pattern = '^' + pattern + '$'
    pattern = re.compile(pattern, flags)
    return lambda s: s if pattern.match(s) is None else None


@title_text_modifier_factory
def re_search_ban(pattern, flags: int=0):
    """
    Constructs modifier that bans explanations whose `target_field` contains a substring that
    matches `pattern` regexp.

    target_field is a kwarg that defaults to 'text'.

    :param pattern: regexp
    :param flags: re construction flags
    :return Modifier
    """
    pattern = re.compile(pattern, flags)
    return lambda s: s if pattern.search(s) is None else None


@modifier_factory
def calculate_key():
    """
    Constructs modifier that fills .key field if it is None.

    :return Modifier
    """

    def apply(e: Explanation):
        if e.key is not None:
            return e
        ret = copy.copy(e)
        ret.key = ExplanationKey.for_explanation(e)
        return ret

    return apply


@modifier_factory
def normalize_title(score_threshold: float=0., delete_if_not_normal: bool=False):
    """
    Constructs modifier that replaces explanation's title with normalized noun if possible.
    Otherwise bans the explanation (returns None).
    score_threshold is used as minimum confidence enough to consider a parse variant.
    :param delete_if_not_normal: specify true if you want to delete explanations if title is not in normal form
    :param score_threshold: enough probability that word is noun
    :return: Modifier
    """

    def apply(e: Explanation):
        new_title = get_valid_noun_initial_form(e.title, score_threshold)
        if new_title is None:
            return None
        if delete_if_not_normal and new_title != e.title:
            return None
        ret = copy.copy(e)
        ret.title = new_title
        return ret

    return apply


@modifier_factory
def ensure_russian_title():
    return lambda e: e if looks_like_valid_russian(e.title) else None


@modifier_factory
def shadow_cognates(length_threshold: int=None, sep_re='\\s+', with_question=False, with_pronoun=False):
    """
    Constructs modifier that splits explanation's text by sep_re regexp and replaces title's cognates with
    GAP_VALUE.

    If length_threshold is specified, the modifier treats any word having with title a common substring of
    at least length_threshold len as cognate.

    Gap can be replaced with default gap value, case quesion or pronoun.
    Use with_question and with_pronoun flags to manipulate it

    :param with_question: specify true if you want to replace gap with question.
            If true is here, value of with_pronoun is ignored
    :param with_pronoun: specify true if you want to replace gap with pronoun
            If with_question is true, this param is ignored
    :param length_threshold: length of the common substring to decide words are cognates
    :param sep_re: separators reg expression
    :return: Modifier
    """
    if isinstance(sep_re, (str, bytes)):
        sep_re = re.compile(sep_re)

    def apply(e: Explanation):
        ret = copy.copy(e)
        for w in sep_re.split(ret.text):
            if with_question:
                gap = '*' + replace_noun_with_question(w, default=GAP_VALUE.strip('*')) + '*'
            elif with_pronoun:
                gap = '*' + replace_noun_with_pronoun(w, default=GAP_VALUE.strip('*')) + '*'
            else:
                gap = GAP_VALUE
            if are_cognates(w, e.title, length_threshold=length_threshold):
                ret.text = re.sub('(^|(?<={notalph})){badword}($|(?={notalph}))'.format(badword=w, notalph=NOTALPH_RE),
                                  gap,
                                  ret.text)
        return ret

    return apply


@modifier_factory
def choose_normal_words_in_explanation(separator: str):
    def apply(e: Explanation):
        ret = copy.copy(e)
        new_list = [w for w in e.text.split(separator)
                    if get_valid_noun_initial_form(w) is not None]
        if len(new_list) == 0:
            return None
        ret.text = separator.join(new_list)
        return ret

    return apply


@modifier_factory
def delete_cognates(length_threshold: int, separator: str):
    def apply(e: Explanation):
        ret = copy.copy(e)
        new_list = [w for w in e.text.split(separator)
                    if not are_cognates(w, e.title, length_threshold)]
        if len(new_list) == 0:
            return None
        ret.text = separator.join(new_list)
        return ret

    return apply


@modifier_factory
def check_contains_valid_parts(required, enough_score, sep_re):
    def apply(e: Explanation):
        have = 0
        for word in re.split(sep_re, e.text):
            if len(word) > 0 and is_remarkable(word, enough_score):
                have += 1
        if have >= required:
            return e
        else:
            return None

    return apply


@modifier_factory
def delete_multiple_gaps(limit: int):
    def apply(e: Explanation):
        num = len(re.findall('\*пропуск\*', e.text))
        if num > limit:
            return None
        else:
            return e

    return apply


@modifier_factory
def shadow_title_with_pronoun():
    def apply(e: Explanation):
        ret = copy.copy(e)
        ret.text = re.sub('(^|(?<={notalph})){badword}($|(?={notalph}))'.format(badword=ret.title, notalph=NOTALPH_RE),
                          '*' + replace_noun_with_pronoun(ret.title, GAP_VALUE) + '*', ret.text)
        return ret

    return apply


@modifier_factory
def shadow_title_with_question():
    def apply(e: Explanation):
        ret = copy.copy(e)
        ret.text = re.sub('(^|(?<={notalph})){badword}($|(?={notalph}))'.format(badword=ret.title, notalph=NOTALPH_RE),
                          '*' + replace_noun_with_question(ret.title, GAP_VALUE) + '*', ret.text)
        return ret

    return apply


@modifier_factory
def calculate_prior_frequency_rate(sep_re):
    def apply(e: Explanation):
        frequents = list(map(get_average_frequency, re.split(sep_re, e.text)))
        frequents.append(get_average_frequency(e.title))
        e.prior_rating = sum(frequents) / len(frequents)
        return e

    return apply


@modifier_factory
def remove_to_much_gap_percentage(sep_re, re_gap, limit):
    def apply(e: Explanation):
        gaps_count = len(re.findall(re_gap, e.text))
        words_count = len([w for w in re.split(sep_re, e.text) if len(w) > 0])
        if gaps_count / words_count < limit:
            return e
        else:
            return None

    return apply
