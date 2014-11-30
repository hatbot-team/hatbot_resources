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
    assets = os.listdir(ASSETS_DIR)
    storages = list()
    for storage_name in assets:
        storage_name = storage_name[:-6]
        storages.append(storage_name)
    return storages