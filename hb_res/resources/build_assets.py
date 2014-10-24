from  .Resource import names_registered, resource_by_name

def build():
    for name in names_registered():
        resource = resource_by_name(name)()
        for explanation in resource:
            r = explanation
            for functor in resource.modifiers:
                r = functor(r)
            # write res in file 'name'
            print(r)
