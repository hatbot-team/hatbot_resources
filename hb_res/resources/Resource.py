__author__ = 'skird'


class Resource:
    """
    Interface of abstract readable/writeable resource
    """

    def entries(self):
        return NotImplementedError

    def add_entry(self, entry) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError