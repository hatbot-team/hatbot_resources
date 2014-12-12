from hb_res.explanations import ExplanationKey

__author__ = 'moskupols'

SEPARATOR = '\t'


class Explanation:
    """
    This class is representation of explanation in resource modules.
    Explanation is defined as tuple of (title, text, key, prior_rating).
    It's essential for both title and text not to contain substring equal to '\t' in any part.
    """

    def __init__(self, title: str, text: str, key: ExplanationKey=None, prior_rating: float=None) -> None:
        """
        Creates explanation from its attributes
        It's essential for explanation not to contain '\t' symbol in any part
        :param title: word to explain
        :param text: explanation itself
        :param key: unique key of explanation
        :param prior_rating: real value of rating
        :return:
        """
        self.prior_rating = prior_rating
        self.key = key
        self.text = text
        self.title = title

    def encode(self) -> str:
        """
        Returns a string which can be decoded back to explanation
        :rtype: str
        :return: string containing attributes of explanation separated by SEPARATOR
        """
        assert SEPARATOR not in self.title, \
            '{} should not contain {!r}, but {!r} contains'.format('Title', SEPARATOR, self.title)
        assert SEPARATOR not in self.text, \
            '{} should not contain {!r}, but {!r} contains'.format('Text', SEPARATOR, self.text)
        return SEPARATOR.join(map(str, (self.title, self.text, self.key, self.prior_rating)))

    @classmethod
    def decode(cls, representation: str):
        """
        decodes explanation from its representation
        :param representation: string containing attributes of explanation separated by SEPARATOR
        :rtype: Explanation
        :return:
        """
        values = representation.split(SEPARATOR)
        assert len(values) == 4, \
            'Encoded explanation should contain exactly 3 occurrences of {!r}, not {}, as in {!r}' \
            .format(SEPARATOR, len(values) - 1, representation)
        values[2] = None if values[2] == 'None' else ExplanationKey.decode(values[2])
        values[3] = None if values[3] == 'None' else float(values[3])
        return cls(*values)

    def __repr__(self):
        return '<Explanation({0.title!r}, {0.text!r}, {0.key!r}, {0.prior_rating!r})>'.format(self)

    def __str__(self) -> str:
        """
        Get exact text representation of explanation
        :rtype: str
        :return: representation string
        """
        return self.encode()

    def __eq__(self, other):
        return isinstance(other, Explanation) and \
            (self.title, self.text, self.key, self.prior_rating) == \
            (other.title, other.text, other.key, other.prior_rating)

    def __hash__(self):
        return hash((self.title, self.text, self.key, self.prior_rating))

    def __lt__(self, other):
        return (self.title, self.text, self.key, self.prior_rating) < \
               (other.title, other.text, other.key, other.prior_rating)
