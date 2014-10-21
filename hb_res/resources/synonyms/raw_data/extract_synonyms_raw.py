__author__ = 'Алексей'

import codecs
from hb_res.resources.synonyms import import_from_site

f = codecs.open('synonyms_raw.txt', mode='w', encoding='utf-8')
site = 'http://synonymonline.ru/'
import_from_site(site, f)
