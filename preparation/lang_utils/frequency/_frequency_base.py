__author__ = 'shkiper'

import os
import codecs

PATH = os.path.dirname(os.path.abspath(__file__)) + '/freq_filtered.dat'


def init_frequency():
    global frequency
    global total_number
    frequency_file = codecs.open(PATH, "r", "utf-8")
    for line in frequency_file:
        word, number = line.split(' ')
        frequency[word] = int(number)
        total_number += int(number)


frequency = dict()
total_number = 0
init_frequency()