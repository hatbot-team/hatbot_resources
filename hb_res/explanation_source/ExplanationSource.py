from hb_res.explanations import Explanation
from hb_res.storage import get_storage

__author__ = 'pershik'


class ExplanationSource:

    def __init__(self, storage_name: str):
        self._name = storage_name
        self.explanations_by_name = dict()
        self.explanations_by_key = dict()
        self.storage = get_storage(storage_name)
        for explanation in self.storage.entries():
            self.explanations_by_key[explanation.key] = explanation
            if explanation.title not in self.explanations_by_name:
                self.explanations_by_name[explanation.title] = list()
            self.explanations_by_name[explanation.title].append(explanation)

    def explain(self, word: str)->list:
        """
        Returns list of Explanation for the given word.

        :param word: russian noun in the initial form, in lowercase.
        :return: list of Explanation
        """
        if word in self.explanations_by_name:
            return self.explanations_by_name[word]
        else:
            return list()

    @property
    def name(self)->str:
        return self._name

    def produces_key(self, key)->bool:
        return key in self.explanations_by_key

    def word_for_key(self, key)->str:
        if key in self.explanations_by_key:
            return self.explanations_by_key[key]
        else:
            return None

    def explanation_for_key(self, key)->Explanation:
        """
        This method is used to return Explanation by its key

        :param key: key generated by keys_for_word
        :return: string containing end user representation of the explanation
        """
        if key in self.explanations_by_key[key]:
            return self.explanations_by_key[key]
        else:
            return None

    def keys_for_word(self, word: str)->list:
        """
        This method is used by explain to initialize Explanations list. It should return a list of
        keys objects. Each of them has to be enough for text_for_key to make the explanation text.

        :param word: the russian lowercase word to be explained
        """
        res = list()
        for explanation in self.explanations_by_name[word]:
            res.append(explanation.key)
        return res

    def explainable_words(self):
        """
        Generates all words explainable using this source.
        :return: Iterable of explainable words
        """
        return self.explanations_by_name.keys()

    def rate_for_key(self, key):
        """
        Returns explanation rate for current explanation
        :return: explanation prior rating
        """
        return self.explanation_for_key(key).prior_rating