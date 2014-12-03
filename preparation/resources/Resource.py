import time

__author__ = "mike"

_resource_blacklist = {'Resource'}
_registered_resources = dict()
_built_resources = set()
_building_resources = set()

from hb_res.storage import get_storage
from copy import copy


def build_deps(res_obj):
    assert hasattr(res_obj, 'dependencies')
    for dep in res_obj.dependencies:
        assert dep + 'Resource' in _registered_resources
        assert dep not in _building_resources, \
            'Dependency loop encountered: {} depends on {} to be built, and vice versa'.format(
                dep + 'Resource', res_obj.__class__.__name__)
        _registered_resources[dep + 'Resource']().build()


def applied_modifiers(res_obj):
    for explanation in res_obj:
        r = copy(explanation)
        for functor in res_obj.modifiers:
            if r is None:
                break
            r = functor(r)
        if r is not None:
            yield r


def generate_asset(res_obj, out_storage):
    out_storage.clear()
    count = 0
    for explanation in applied_modifiers(res_obj):
        count += 1
        print(count, end='\r')
        out_storage.add_entry(explanation)
    return count


def resource_build(res_obj):
    res_name = res_obj.__class__.__name__
    assert res_name.endswith('Resource')
    res_name = res_name[:-len('Resource')]

    if res_name in _built_resources:
        print("= Skipping {} generation as the resource is already built".format(res_name))
        return

    _building_resources.add(res_name)
    build_deps(res_obj)

    print("<=> Starting {} generation <=>".format(res_name))
    start = time.monotonic()
    with get_storage(res_name) as out_storage:
        count = generate_asset(res_obj, out_storage)
    end = time.monotonic()
    print("> {} generated in {} seconds".format(res_name, end - start))
    print("> {} explanations have passed the filters".format(count))

    _building_resources.remove(res_name)
    _built_resources.add(res_name)


class ResourceMeta(type):
    """
    metaclass for classes which represent resource package
    """

    def __new__(mcs, name, bases, dct):
        """
        we have to register resource in _registered_resources
        """
        global _registered_resources
        if name in _registered_resources.keys():
            raise KeyError('Resource with name {} is already registered'.format(name))

        old_iter = dct['__iter__']

        def iter_wrapped(self):
            build_deps(self)
            return old_iter(self)

        dct['build'] = resource_build
        dct['__iter__'] = iter_wrapped

        res = super(ResourceMeta, mcs).__new__(mcs, name, bases, dct)
        if name not in _resource_blacklist:
            _registered_resources[name] = res
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


def names_registered():
    global _registered_resources
    return _registered_resources.keys()


def resources_registered():
    global _registered_resources
    return _registered_resources.values()


def resource_by_name(name) -> Resource:
    """
    Returns resource described by its name
    :param name: name of desired resource
    :return: iterable resource as list of strings
    """
    global _registered_resources
    resource = _registered_resources.get(name, None)
    if resource is None:
        raise KeyError('Unknown resource {}'.format(name))
    return resource
