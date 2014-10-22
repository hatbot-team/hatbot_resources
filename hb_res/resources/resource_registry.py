from hb_res.resources.Resource import Resource

__author__ = 'skird'

_registered_resources = dict()


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


def register_resource(name, resource) -> None:
    """
    Register resource object
    :param name: name to assign
    :param resource: iterable object
    """
    global _registered_resources
    if name in _registered_resources.keys():
        raise KeyError('Resource with name {} is already registered'.format(name))
    _registered_resources[name] = resource


def names_registered():
    global _registered_resources
    return _registered_resources.keys()


def resources_registered():
    global _registered_resources
    return _registered_resources.values()
