__author__ = 'skird'

from os import path
import readline
from hb_res.explanation_source import sources_registry, ExplanationSource

SEPARATOR = '\t'
DIR_PATH = path.dirname(path.abspath(__file__))
SELECTED_FILE = 'Selected.asset'
GOOD_WORDS_FILE = 'goodwords.dat'
ALL_SOURCES = sources_registry.sources_registered()


def explain_list(word):
    explanations = list()
    for source in ALL_SOURCES:
        for e in source.explain(word):
            explanations.append((e, source.name))
    return explanations

selected = set()
for line in open(path.join(DIR_PATH, SELECTED_FILE)):
    selected.add(line.strip().split('\t')[0])

asset_desc = open(path.join(DIR_PATH, SELECTED_FILE), 'a')
selected_in_session = 0
for word in open(path.join(DIR_PATH, GOOD_WORDS_FILE)):
    word = word.strip()
    if word in selected:
        continue
    print('{} selected words'.format(len(selected) + selected_in_session))
    explanations = explain_list(word)
    print('Объясняю слово: {}'.format(word))
    cnt = 1
    for e, asset in explanations:
        print('{}. {} (from {})'.format(cnt, e.text, asset))
        cnt += 1

        answer = ''
        while answer.lower() != 'y' and answer.lower() != 'n' and answer.lower() != 'c':
            answer = input('Берем? Исправляем? [Y/N/C] ')

        if answer == 'y':
            print(e.encode(), file=asset_desc)
        elif answer == 'c':
            new_text = ''
            while new_text.strip() == '':
                readline.set_startup_hook(lambda: readline.insert_text(e.text))
                try:
                    new_text = input('Новый текст: ')
                finally:
                    readline.set_startup_hook()
            e.text = new_text
            print(e.encode(), file=asset_desc)

    selected_in_session += 1
    answer = ''
    while answer.lower() != 'y' and answer.lower() != 'n':
        answer = input('Еще? [Y/N] ')
    if answer.lower() == 'n':
        break

print('{} words filtered so for. Bye'.format(selected_in_session))
