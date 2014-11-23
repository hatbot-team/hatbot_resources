from preparation.resources import Resource

resource_packages = [
    'synonyms', 'antonyms', 'definitions', 'phraseological',
    'film_titles', 'collocations', 'crosswords', 'book_titles', 'solance'
]
__all__ = [
    'Resource'
]

for module in resource_packages:
    globals()[module] = __import__(__name__ + '.' + module)
