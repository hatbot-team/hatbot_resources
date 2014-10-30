resource_packages = [
    'SampleResource'
]
__all__ = [
    'Resource'
]

for module in resource_packages:
    globals()[module] = __import__(__name__ + '.' + module)

from . import Resource
