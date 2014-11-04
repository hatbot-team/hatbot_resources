"""
Common modifiers for use in resources.
"""
import itertools
import re
import copy

from hb_res.explanations import Explanation, ExplanationKey
from preparation.lang_utils.cognates import are_cognates
from preparation.lang_utils.morphology import get_valid_noun_initial_form

GAP_VALUE = '###'


class Modifier:
    def __init__(self, *args, _name=None, **kwargs):
        if _name is None:
            _name = self.__name__
        self.__repr = '<modifier {}({})>'.format(
            _name,
            ', '.join(itertools.chain(
                map(repr, args),
                itertools.starmap('{}={!r}'.format, kwargs.items())
            ))
        )

    def __repr__(self):
        return self.__repr

    def __call__(self, e: Explanation):
        raise NotImplementedError


def modifier_factory(factory, name=None):
    if name is None:
        name = factory.__name__

    class DecoratedModifier(Modifier):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, _name=name, **kwargs)
            self._mod = factory(*args, **kwargs)

        def __call__(self, e):
            return self._mod(e)

    return DecoratedModifier


def title_text_modifier_factory(factory, name=None):
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
    return lambda s: s.strip(chars)


@title_text_modifier_factory
def re_replace(pattern: str, replacement: str, flags: int=0):
    pattern = re.compile(pattern, flags)
    return lambda s: pattern.sub(replacement, s)


@title_text_modifier_factory
def re_fullmatch_ban(pattern: str, flags: int=0):
    return lambda s: s if re.fullmatch(pattern, s, flags) is None else None


@modifier_factory
def calculate_key():
    def apply(e: Explanation):
        if e.key is not None:
            return e
        ret = copy.copy(e)
        ret.key = ExplanationKey.for_text(ret.text)
        return ret
    return apply


@modifier_factory
def normalize_title(score_threshold: float=0.):
    def apply(e: Explanation):
        new_title = get_valid_noun_initial_form(e.title, score_threshold)
        if new_title is None:
            return None
        ret = copy.copy(e)
        ret.title = new_title
        return ret
    return apply


@modifier_factory
def shadow_cognates(length_threshold: int=None, sep_re: str='\\s+'):
    sep_re = re.compile(sep_re)

    def apply(e: Explanation):
        ret = copy.copy(e)
        for w in sep_re.split(ret.text):
            if are_cognates(w, e.title, length_threshold=length_threshold):
                ret.text = re.sub(w, GAP_VALUE, ret.text, flags=re.IGNORECASE)
        return ret
    return apply
