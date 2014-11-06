__author__ = 'skird'


class ExplanationStorage:
    """
    Interface of abstract readable/writeable resource.
    Every resource is a map from string to list of strings.
    It supports random access and provides iterator on its elements.
    It is closeable.

    `With' statement is supported out of the box, expecting that all
    preparation has been completed at initialization time.
    """

    def entries(self):
        raise NotImplementedError

    def add_entry(self, entry) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError

    def __enter__(self):
        """ Default implementation of context manager enter. Does nothing. """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Default implementation of context manager exit. Calls close. """
        self.close()
        return False
