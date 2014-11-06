from copy import copy

from preparation.resources.Resource import names_registered, resource_by_name
from hb_res.storage import get_storage


def rebuild_from_resource(resource_name: str):
    resource = resource_by_name(resource_name)()
    out_storage = get_storage(resource_name.replace('Resource', ''))
    out_storage.clear()
    for explanation in resource:
        r = copy(explanation)
        for functor in resource.modifiers:
            if r is None:
                break
            r = functor(r)
        if r is not None:
            out_storage.add_entry(r)
    out_storage.close()


def rebuild_all():
    for name in names_registered():
        rebuild_from_resource(name)