from preparation.resources.Resource import gen_resource


@gen_resource('SampleResource', [])
def read_all():
    yield None
