__author__ = 'moskupols'


__all__ = ['ExplanationStorage', 'get_storage', 'list_storages']


from . ExplanationStorage import ExplanationStorage
from . FileExplanationStorage import FileExplanationStorage
import os

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))


def get_storage(trunk: str):
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
    return FileExplanationStorage(os.path.join(ASSETS_DIR, trunk + '.asset'))


def list_storages():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
    return os.listdir(ASSETS_DIR)