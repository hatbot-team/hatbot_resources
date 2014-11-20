__author__ = 'pershik'

import requests
import json

PREFIX = 'http://solance.me/search?findme='
SUFFIX = '&translate=ru&langs[]=ru'


def get_consonance(word):
    request = PREFIX + word + SUFFIX
    answer = json.loads(requests.get(request).text, encoding='utf-8')
    array = answer.get('array').get('ru')
    consonances = list()
    if array is None:
        return consonances
    for expl in array:
        word = expl[0].get('word')
        quality = expl[1]
        consonances.append([word, quality])
    return consonances
