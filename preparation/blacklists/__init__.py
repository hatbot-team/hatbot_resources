from os import path

__author__ = 'moskupols'

_LISTS_DIR = path.dirname(path.abspath(__file__))


def _load_titles(filename):
    with open(path.join(_LISTS_DIR, filename)) as inf:
        return frozenset(w for w in map(str.strip, inf) if len(w))


TITLE_BLACKLIST = _load_titles('title_blacklist.txt')
TITLE_WHITELIST = _load_titles('title_whitelist.txt')
