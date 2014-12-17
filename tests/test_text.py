import unittest

import nose

from tests.trunk_aware import trunk_parametrized, asset_cache


__author__ = 'moskupols'


@trunk_parametrized()
def test_text_starts_with_non_ws(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        case.assertFalse(e.text.startswith(' '), e)


@trunk_parametrized()
def test_text_ends_with_non_ws(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        case.assertFalse(e.text.endswith(' '), e)


@trunk_parametrized()
def test_spaces_after_punct(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        case.assertNotRegex(e.text, r'[!?]\w')
        case.assertNotRegex(e.text, r'[,:;]([^ ]|$)')

        # had to circumvent 'Лента.ру' exception
        case.assertNotRegex(e.text, r'(?<![Лл]ен)[ёа-я]{2}[.][ЁА-Яёа-я]')


@trunk_parametrized()
def test_single_spacing(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        case.assertFalse('  ' in e.text)


@trunk_parametrized()
def test_no_ws_but_space(trunk):
    case = unittest.TestCase()
    for e in asset_cache(trunk):
        case.assertNotRegex(e.text, r'(?! )\s')


if __name__ == '__main__':
    nose.main()
