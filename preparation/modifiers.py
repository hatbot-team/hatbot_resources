"""
Common modifiers for use in resources.
"""

import re
import copy
from hb_res.explanations import Explanation, ExplanationKey
from preparation.lang_utils.cognates import are_cognates
from preparation.lang_utils.morphology import get_valid_noun_initial_form

GAP_VALUE = '###'


class Modifier:
    def __init__(self, *args, **kwargs):
        self.__repr = '{}({})'.format(
            self.__class__,
            ', '.join(list(map(repr, args)) + list(map(repr, kwargs)))
        )

    def __repr__(self):
        return self.__repr

    def __call__(self, e: Explanation):
        raise NotImplementedError


class TitleOrTextModifier(Modifier):
    def __init__(self, *args, target='text', **kwargs):
        super().__init__(*args, target=target, **kwargs)
        if target not in {'text', 'title'}:
            raise ValueError('target should be either "text" or "title"')
        self.target = target

    def __call__(self, e: Explanation):
        ret = copy.copy(e)
        if self.target == 'text':
            self._modify(e.text)
            if e.text is None:
                return None
        else:
            self._modify(e.title)
            if e.title is None:
                return None
        return ret

    def _modify(self, s: str):
        raise NotImplementedError


class Strip(TitleOrTextModifier):
    def __init__(self, chars=None, target='text'):
        super().__init__(chars=chars, target=target)
        self.chars = chars

    def _modify(self, s: str):
        return s.strip(self.chars)


class REReplace(TitleOrTextModifier):
    def __init__(self, pattern: str, replacement: str, flags=0, target='text'):
        super().__init__(pattern, replacement, flags=flags, target=target)
        self.pattern = re.compile(pattern, flags)
        self.replacement = replacement

    def _modify(self, s: str):
        return self.pattern.sub(self.replacement, s)


class REFullmatchBan(TitleOrTextModifier):
    def __init__(self, pattern: str, flags=0, target='text'):
        super().__init__(pattern, flags=flags, target=target)
        self.pattern = pattern
        self.flags = flags

    def _modify(self, s: str):
        return None if re.fullmatch(self.pattern, s, self.flags) is None else s


class CalculateKey(Modifier):
    def __init__(self):
        super().__init__()

    def __call__(self, e: Explanation):
        if e.key is not None:
            return e

        ret = copy.copy(e)
        ret.key = ExplanationKey.for_text(e.text)
        return ret


class NormalizeTitle(Modifier):
    def __init__(self, score_threshold=0.):
        super().__init__(score_threshold=score_threshold)
        self.score_threshold = score_threshold

    def __call__(self, e: Explanation):
        ret = copy.copy(e)
        ret.title = get_valid_noun_initial_form(e.title, self.score_threshold)
        return None if ret.title is None else ret


class ShadowCognates(Modifier):
    def __init__(self, length_threshold: int=None, sep_re='\\s+'):
        super().__init__(length_threshold=length_threshold, sep_re=sep_re)
        self.sep_re = re.compile(sep_re)
        self.length_threshold = length_threshold

    def __call__(self, e: Explanation):
        ret = copy.copy(e)
        for w in self.sep_re.split(ret.text):
            if are_cognates(w, e.title, length_threshold=4):
                ret.text = re.sub(w, GAP_VALUE, ret.text, flags=re.IGNORECASE)
        return ret
