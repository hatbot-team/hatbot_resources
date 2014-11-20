__author__ = 'pershik'

import codecs
from preparation.resources.solance.raw_data import extractor


def extract_all():
    file = codecs.open("solance_raw.txt", mode='w', encoding='utf-8')
    words_file = codecs.open("words.txt", mode='r', encoding='utf-8')
    words = words_file.read().split('\n')
    print(len(words))
    counter = 0
    for word in words:
        counter += 1
        if counter % 200 == 0:
            print(counter)
        consonances = extractor.get_consonance(word)
        if len(consonances) != 0:
            file.write(word + "@")
            for consonance in consonances:
                file.write(consonance[0] + "&" + str(consonance[1]) + "#")
            file.write('\n')
    file.close()
    words_file.close()

extract_all()
