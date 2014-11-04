__author__ = 'moskupols'

__all__ = ['get_parts_of_speech', 'get_initial_forms', 'get_valid_noun_initial_form', 'morph']

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

from .word_forms import get_valid_noun_initial_form, get_initial_forms
from .parts_of_speech import get_parts_of_speech
