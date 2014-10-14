__author__ = 'Алексей'

import codecs
from resources.synonyms import import_from_site

f = codecs.open('antonyms_raw.txt', mode='w', encoding='utf-8')
site = 'http://antonymonline.ru/'
import_from_site(site, f)