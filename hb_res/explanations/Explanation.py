from hb_res.explanations import ExplanationKey

__author__ = 'moskupols'

SEPARATOR = '\t'


class Explanation:
    """
    This class is representation of explanation in resource modules
    Explanation is defined at tuple of (title, text, key, prior_rating)
    It's essential for explanation not to contain substring equal to SEPARATOR in any part
    """

    def __init__(self, title, text, key=None, prior_rating=None) -> None:
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
        return SEPARATOR.join((self.title, self.text, str(self.key), str(self.prior_rating)))

    @classmethod
    def decode(cls, representation):
        """
        decodes explanation from its representation
        :param representation: string containing attributes of explanation separated by SEPARATOR
        :rtype: Explanation
        :return:
        """
        values = representation.split(SEPARATOR)
        if values[3] == 'None':
            values[3] = None
        return Explanation(values[0], values[1], ExplanationKey.decode(values[2]), float(values[3]))

    def __repr__(self) -> str:
        """
        Get exact text representation of explanation
        :rtype: str
        :return: representation string
        """
        return self.encode()
