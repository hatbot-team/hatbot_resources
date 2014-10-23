__autor__ = "mike"

_resource_blacklist={'Resource'}
_registered_resources = dict()

class ResourceMeta(type):
    """
    metaclass for classes which represent resource package
    """
    def __new__(cls, name, bases, dct):
        """
        we have to register resource in _registered_resources
        """
        global __registered_resources
        if name in _registered_resources.keys():
            raise KeyError('Resource with name {} is already registered'.format(name))
        res = super(__class__, cls).__new__(cls, name, bases, dct)
        if name not in _resource_blacklist:
            _registered_resources[name] = res
            # because we don't want to add base class to _registered_resources
        return res

class Resource(metaclass=ResourceMeta):
    modifiers = []
    def __iter__(self):
        raise NotImplementedError

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
