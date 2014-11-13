__author__ = 'pershik'


def diff(title=None, resource=None, explanations=None,
         first_modifiers=None, second_modifiers=None):

    from hb_res.explanations import Explanation
    from preparation.resources.Resource import resource_by_name

    def apply(explanation, modifiers):
        for modifier in modifiers:
            explanation = modifier(explanation)
        return explanation

    def get_diff(expl, first_modifiers, second_modifiers):
        first_expl = apply(expl, first_modifiers)
        second_expl = apply(expl, second_modifiers)
        if first_expl.encode() == second_expl.encode():
            return tuple((first_expl, second_expl))
        else:
            return None

    if isinstance(resource, str):
        resource = resource_by_name(resource)()

    assert first_modifiers is not None or hasattr(resource, 'modifiers')
    if first_modifiers is None:
        first_modifiers = resource.modifiers
    assert second_modifiers is not None

    assert (title is not None and resource is not None) ^ (explanations is not None)
    if explanations is None:
        explanations = (e for e in resource if e.title == title)

    if isinstance(explanations, Explanation):
        difference = get_diff(explanations, first_modifiers, second_modifiers)
        if difference is not None:
            return list(difference)
        else:
            return list()
    else:
        res = list()
        for expl in explanations:
            difference = get_diff(expl, first_modifiers, second_modifiers)
            if difference is not None:
                res.append(difference)
        return res


def main(args=None):
    return


if __name__ == '__main__':
    main()