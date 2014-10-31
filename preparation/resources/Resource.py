__author__ = "mike"

_resource_blacklist = {'Resource'}
_registered_resources = dict()


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
        res = super(ResourceMeta, mcs).__new__(mcs, name, bases, dct)
        if name not in _resource_blacklist:
            _registered_resources[name] = res
        return res


class Resource(metaclass=ResourceMeta):
    def __iter__(self):
        raise NotImplementedError


def gen_resource(res_name, modifiers):
    def decorator(func):
        def __init__(self):
            self.modifiers = modifiers

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
