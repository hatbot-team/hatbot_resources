from  .Resource import names_registered, resource_by_name

def build():
    for name in names_registered():
        resource = resource_by_name(name)()
        print(name)
        for explanation in resource:
            res = explanation
            for functor in resource.modifiers:
                res = functor(res)
            # write res in file 'name'
            print(res)
