from hb_res.resources.Resource import Resource


class SampleResource(Resource):
    def __iter__(self):
        def read_all():
            yield None
        return read_all()
