__author__ = 'moskupols'

__all__ = ['get_parts_of_speech', 'get_initial_forms', 'get_valid_noun_initial_form', 'morph', 'is_remarkable']

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

from .word_forms import get_valid_noun_initial_form, get_initial_forms
from .parts_of_speech import get_parts_of_speech
from .parts_of_speech import is_remarkable
from .replace_with_gap import replace_noun_with_pronoun, replace_noun_with_question