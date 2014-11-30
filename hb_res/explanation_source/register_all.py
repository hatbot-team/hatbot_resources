from hb_res.explanation_source import ExplanationSource
from hb_res.explanation_source.sources_registry import register_source
from hb_res.storage import list_storages

__author__ = 'pershik'

for storage_name in list_storages():
    register_source(ExplanationSource(storage_name))
