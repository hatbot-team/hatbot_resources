from copy import copy
from hb_res.explanations import Explanation
from preparation.resources.Resource import resource_by_name

__author__ = 'moskupols'


def evolution(title=None, resource=None, *, modifiers=None, explanations=None):
    def evolute(expl, mods):
        c = copy(expl)
        yield ('', c)
        for m in mods:
            c = m(c)
            yield (m, c)
            if c is None:
                break

    if isinstance(resource, str):
        resource = resource_by_name(resource)()

    assert modifiers is not None or hasattr(resource, 'modifiers')
    if modifiers is None:
        modifiers = resource.modifiers

    assert (title is not None and resource is not None) ^ (explanations is not None)
    if explanations is None:
        explanations = filter(lambda e: e.title == title, resource)

    if isinstance(explanations, Explanation):
        yield tuple(evolute(explanations, modifiers))
    else:
        for e in explanations:
            yield (e, tuple(evolute(e, modifiers)))
