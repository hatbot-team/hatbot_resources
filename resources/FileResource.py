from resources.Resource import Resource

__author__ = 'skird'


class FileResource(Resource):
    """
    Class representing text resource connected with some file
    """

    def __init__(self, path_to_file):
        self.file_name = path_to_file
        self.descriptor = open(self.file_name, 'a')

    def entries(self):
        return open(self.file_name)

    def add_entry(self, entry) -> None:
        print(entry, file=self.descriptor)

    def clear(self) -> None:
        self.descriptor = open(self.file_name, 'w')