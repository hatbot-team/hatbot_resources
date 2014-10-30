__author__ = 'moskupols'


__all__ = ['ExplanationStorage', 'get_storage']


from . ExplanationStorage import ExplanationStorage
from . FileExplanationStorage import FileExplanationStorage
from os import path

ASSETS_DIR = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..', 'assets'))


def get_storage(trunk: str):
    return FileExplanationStorage(path.join(ASSETS_DIR, trunk + '.asset'))
