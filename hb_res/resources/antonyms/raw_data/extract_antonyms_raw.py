import codecs
from hb_res.resources.synonyms import import_from_site

__author__ = 'Алексей'


f = codecs.open('antonyms_raw.txt', mode='w', encoding='utf-8')
site = 'http://antonymonline.ru/'
import_from_site(site, f)
