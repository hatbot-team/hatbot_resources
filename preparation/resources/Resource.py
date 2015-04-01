from hb_res.storage import get_storage
from copy import copy
import time

__author__ = "mike"

_resource_blacklist = {'Resource'}
_resources_by_trunk = dict()
_built_trunks = set()
_building_trunks = set()


def build_deps(res_obj):
    assert hasattr(res_obj, 'dependencies')
    for dep in res_obj.dependencies:
        assert dep in _resources_by_trunk
        assert dep not in _building_trunks, \
            'Dependency loop encountered: {} depends on {} to be built, and vice versa'.format(
                dep, res_obj.__class__.__name__)
        _resources_by_trunk[dep]().build()


def applied_modifiers(res_obj):
    generated = set()
    for explanation in res_obj:
        r = copy(explanation)
        for functor in res_obj.modifiers:
            if r is None:
                break
            r = functor(r)
        if r is not None and r not in generated:
            generated.add(r)
            yield r


def generate_asset(res_obj, out_storage):
    out_storage.clear()
    count = 0
    for explanation in applied_modifiers(res_obj):
        if count % 100 == 0:
            print(count, end='\r')
        count += 1
        out_storage.add_entry(explanation)
    return count


def resource_build(res_obj):
    trunk = res_obj.trunk

    if trunk in _built_trunks:
        print("= Skipping {} generation as the resource is already built".format(trunk))
        return

    _building_trunks.add(trunk)
    build_deps(res_obj)

    print("<=> Starting {} generation <=>".format(trunk))
    start = time.monotonic()
    with get_storage(trunk) as out_storage:
        count = generate_asset(res_obj, out_storage)
    end = time.monotonic()
    print("> {} generated in {} seconds".format(trunk, end - start))
    print("> {} explanations have passed the filters".format(count))

    _building_trunks.remove(trunk)
    _built_trunks.add(trunk)


class ResourceMeta(type):
    """
    metaclass for classes which represent resource package
    """

    def __new__(mcs, name, bases, dct):
        """
        we have to register resource in _registered_resources
        """
        assert name.endswith('Resource')
        trunk = name[:-len('Resource')]

        global _resources_by_trunk
        if trunk in _resources_by_trunk.keys():
            raise KeyError('Resource with name {} is already registered'.format(name))

        old_iter = dct['__iter__']

        def iter_wrapped(self):
            build_deps(self)
            return old_iter(self)

        @property
        def trunk_prop(_):
            return trunk

        dct['trunk'] = trunk_prop
        dct['build'] = resource_build
        dct['__iter__'] = iter_wrapped

        res = super(ResourceMeta, mcs).__new__(mcs, name, bases, dct)
        if name not in _resource_blacklist:
            _resources_by_trunk[trunk] = res
        return res


class Resource(metaclass=ResourceMeta):
    def __iter__(self):
        raise NotImplementedError


def gen_resource(res_name, modifiers, dependencies=()):
    def decorator(func):
        def __init__(self):
            self.modifiers = modifiers
            self.dependencies = dependencies

        def __iter__(self):
            return iter(func())

        ResourceMeta(res_name, tuple(), {'__iter__': __iter__, '__init__': __init__})

    return decorator


def trunks_registered():
    global _resources_by_trunk
    return _resources_by_trunk.keys()


def resources_registered():
    global _resources_by_trunk
    return _resources_by_trunk.values()


def resource_by_trunk(name) -> Resource:
    """
    Returns resource described by its name
    :param name: name of desired resource
    :return: iterable resource as list of strings
    """
    global _resources_by_trunk
    resource = _resources_by_trunk.get(name, None)
    if resource is None:
        raise KeyError('Unknown resource {}'.format(name))
    return resource
