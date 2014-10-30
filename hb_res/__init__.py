__author__ = 'moskupols'

from ._essential_packages import ESSENTIAL_PACKAGES

try:
    from ._extra_packages import EXTRA_PACKAGES
except ImportError:
    EXTRA_PACKAGES = []
    pass

__all__ = ESSENTIAL_PACKAGES + EXTRA_PACKAGES

for pack in __all__:
    globals()[pack] = __import__(__name__ + '.' + pack)
