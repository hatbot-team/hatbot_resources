from copy import copy

from .Resource import names_registered, resource_by_name
from hb_res.resources.FileExplanationStorage import FileExplanationStorage as Storage


def rebuild_from_resource(resource_name: str):
    resource = resource_by_name(resource_name)()
    with Storage(resource_name.replace('Resource', 'Storage')) as out_storage:
        out_storage.clear()
        for explanation in resource:
            r = copy(explanation)
            for functor in resource.modifiers:
                if r is None:
                    break
                r = functor(r)
            if r is not None:
                out_storage.add_entry(r)


def rebuild_all():
    map(rebuild_from_resource, names_registered())
