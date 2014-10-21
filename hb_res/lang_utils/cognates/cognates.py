from hb_res.lang_utils.cognates import _cognates_base
from hb_res.lang_utils.morphology import get_initial_forms

__author__ = 'Oktosha'


def get_roots(word):
    """
    Returns list of root-words which are titles of dictionary articles containing the given word.
    If the dictionary doesn't contain the given word the list containing word itself is returned.

    :param word: russian word
    :return: list of root-words
    """
    """
    :param word:
    :return:
    """
    if word in _cognates_base.cognates:
        return _cognates_base.cognates[word]
    else:
        return [word]


def are_cognates(a, b, length_threshold=None):
    """
    Checks two words for having same root.
    If length_threshold specified words are considered cognates if they
    contain common substring of length at least as threshold

    >>> are_cognates('мама', 'рама')
    False
    >>> are_cognates('мама', 'маме')
    True
    >>> are_cognates('мама', 'маменька')
    True
    >>> are_cognates('авиация', 'авиамотор', length_threshold=4)
    True
    >>> are_cognates('цивилизация', 'цыганизация', length_threshold=5) # beware...
    True

    :param a: string containing russian word
    :param b: same as a
    :param length_threshold: minimal size of forbidden common substring
    :return: True if a and b are possibly cognates, False otherwise.
    """
    a, b = a.lower(), b.lower()
    a, b = a.replace('ё', 'е'), b.replace('ё', 'е')

    a_roots = []
    for word in get_initial_forms(a):
        a_roots.extend(get_roots(word))

    b_roots = []
    for word in get_initial_forms(b):
        b_roots.extend(get_roots(word))

    if not set(a_roots).isdisjoint(b_roots):
        return True

    if length_threshold is not None:
        for i in range(len(a) - length_threshold + 1):
            for j in range(len(b) - length_threshold + 1):
                if a[i: i + length_threshold] == b[j: j + length_threshold]:
                    return True

    return False
