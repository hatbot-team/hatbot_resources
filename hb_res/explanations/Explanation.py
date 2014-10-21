__author__ = 'moskupols'


class Explanation:

    def __init__(self, title, text, key=None, prior_rating=None):
        self.prior_rating = prior_rating
        self.key = key
        self.text = text
        self.title = title
