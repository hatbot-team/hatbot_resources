from hb_res.resources.Resource import gen_resource

@gen_resource('My Resource', [])
def read_all():
    yield None
