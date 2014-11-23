__author__ = 'shkiper'

from ._frequency_base import frequency
from ._frequency_base import total_number


def get_frequent_number(word: str)->int:
    """
    Returns number of occurrences of passed word in literature texts.
    Warning: not normalized, for comparison only.
    :param word: passed word in russian
    :return: non-negative int number
    """
    return frequency.get(word.lower(), 0)


def get_average_frequency(word: str)->int:
    """
    Returns percentage of passed russian word in literature texts.
    :param word: passed word in russian
    :return: float number from segment [0..100]
    """
    return get_frequent_number(word.lower()) / total_number * 100