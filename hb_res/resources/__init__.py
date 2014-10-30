resource_packages = [
                 'SampleResource'
                ]
__all__ = [
        'Resource'
        'build_assets'
        ]

for module in resource_packages:
    globals()[module] = __import__(__name__ + '.' + module)


from . import Resource
from . import build_assets
build_assets.rebuild_all()
