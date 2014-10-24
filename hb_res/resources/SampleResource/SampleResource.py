from hb_res.resources.Resource import resource

@resource('SampleResource', [])
def read_all():
    yield None
