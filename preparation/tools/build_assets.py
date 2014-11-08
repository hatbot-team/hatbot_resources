from copy import copy
import sys

from preparation.resources.Resource import names_registered, resource_by_name
from hb_res.storage import get_storage


def rebuild_from_resource(resource_name: str):
    resource = resource_by_name(resource_name)()
    trunk = resource_name.replace('Resource', '')
    with get_storage(trunk) as out_storage:
        print("Starting {} generation".format(trunk))
        out_storage.clear()
        for explanation in resource:
            r = copy(explanation)
            for functor in resource.modifiers:
                if r is None:
                    break
                r = functor(r)
            if r is not None:
                out_storage.add_entry(r)
        print("Finished {} generation".format(trunk))


def rebuild_all():
    for name in names_registered():
        rebuild_from_resource(name)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("{}: support either resource name or 'all'".format(sys.argv[0]))
    else:
        if sys.argv[1] == 'all':
            rebuild_all()
        else:
            rebuild_from_resource(sys.argv[1])
