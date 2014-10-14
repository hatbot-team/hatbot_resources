__author__ = 'Алексей'

import requests
from bs4 import BeautifulSoup


def get_all_words(address, word, file):
    local_a = requests.get(address)
    local_soup = BeautifulSoup(local_a.text)
    synonyms = [candidate.span.text for candidate in local_soup.find_all('li')]
    file.write(word + '-')
    for synonym in synonyms:
        file.write(synonym + ',')
    file.write('\n')


def import_from_page(site, page_address, f):
    a = requests.get(page_address)
    soup = BeautifulSoup(a.text)
    n = 0
    for local in soup.findAll('li'):
        str1 = str(local.a.attrs['href'])
        get_all_words(site + str1, str1.split('/')[-1], f)
        n += 1
    return n


def import_from_site(site, f):
    for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        n = 1
        while import_from_page(site, site + str(letter) + "?page=" + str(n), f) > 0:
            n += 1