__author__ = 'skird'


class ExplanationStorage:
    """
    Interface of abstract readable/writeable resource
    Every resource is a map from string to list of strings
    It supports random access and provides iterator on its elements
    """

    def entries(self):
        return NotImplementedError

    def add_entry(self, entry) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError