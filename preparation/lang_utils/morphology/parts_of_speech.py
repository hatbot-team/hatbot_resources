from preparation.lang_utils.morphology import morph

__author__ = 'moskupols'


def get_parts_of_speech(word):
    """
    Returns a list strings describing parts of speech the given russian word could be.
    The enums are derived from pymorphy2.

    >>> get_parts_of_speech('рогалик')
    ['NOUN']
    >>> get_parts_of_speech('постовой')
    ['ADJF', 'NOUN']
    >>> 'NOUN' in get_parts_of_speech('правил')
    True
    >>> 'ADJF' in get_parts_of_speech('правил')
    False

    :param word: a russian word
    :return: list of pymorphy2 POS enums.
    """
    met = set()
    ret = []
    for p in morph.parse(word):
        # if p.score < .1:
        #     continue
        pos = p.tag.POS
        if pos not in met:
            ret.append(pos)
            met.add(pos)
    return ret

def is_remarkable(word, required_score):
    """
    Check if word can be a remarkable part of speech (not minor, like preposition)
    :param word: passed word
    :return: True if word can have remarkable part of speech, false otherwise
    """
    valid_parts = {'NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB',
                   'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO'}
    for p in morph.parse(word):
        if p.score > required_score and p.tag.POS in valid_parts:
            return True
    return False