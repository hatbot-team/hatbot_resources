from hb_res.storage import ExplanationStorage
from hb_res.explanations.Explanation import Explanation

__author__ = 'skird'


class FileExplanationStorage(ExplanationStorage):
    """
    Class representing explanation resource connected with some text file
    """

    def __init__(self, path_to_file):
        self.file_name = path_to_file
        self.write_desc = None

    def entries(self):
        if self.write_desc is not None:
            self.write_desc.flush()
        with open(self.file_name, encoding='utf-8') as read_desc:
            for line in read_desc:
                yield Explanation.decode(line.strip())

    def add_entry(self, entry: Explanation) -> None:
        if self.write_desc is None:
            self.write_desc = open(self.file_name, mode='a', encoding='utf-8')
        print(entry, file=self.write_desc)

    def clear(self) -> None:
        if self.write_desc is not None:
            self.write_desc.close()
        self.write_desc = open(self.file_name, mode='w', encoding='utf-8')

    def close(self) -> None:
        if self.write_desc is not None:
            self.write_desc.close()

    def __getitem__(self, key):
        for explanation in self.entries():
            if explanation.key == key:
                return explanation
