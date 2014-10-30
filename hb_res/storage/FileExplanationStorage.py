from hb_res.storage import ExplanationStorage

__author__ = 'skird'

import codecs
from hb_res.explanations.Explanation import Explanation


class FileExplanationStorage(ExplanationStorage):
    """
    Class representing explanation resource connected with some text file
    """

    def __init__(self, path_to_file):
        self.file_name = path_to_file
        self.descriptor = codecs.open(self.file_name, mode='a', encoding='utf-8')

    def entries(self):
        self.descriptor.flush()
        for line in open(self.file_name):
            yield Explanation.decode(line.strip())

    def add_entry(self, entry: Explanation) -> None:
        print(entry, file=self.descriptor)

    def clear(self) -> None:
        self.descriptor = codecs.open(self.file_name, mode='w', encoding='utf-8')

    def close(self) -> None:
        self.descriptor.flush()

    def __getitem__(self, key):
        for explanation in self.entries():
            if explanation.key == key:
                return explanation
