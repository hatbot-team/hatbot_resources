from preparation.resources import Resource

resource_packages = [
    'synonyms', 'antonyms'
]
__all__ = [
    'Resource'
]

for module in resource_packages:
    globals()[module] = __import__(__name__ + '.' + module)
