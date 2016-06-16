import os
import site
import sys
from distutils.sysconfig import get_python_lib

NON_USERDEFINED_PATHES = [get_python_lib(standard_lib=True, prefix=os.path.realpath(sys.prefix)),
                          get_python_lib(standard_lib=True), ]

try:
    NON_USERDEFINED_PATHES += site.getsitepackages()
except AttributeError:
    pass


def dumps(m):
    return m.__name__


def loads(b):
    if "." in b:
        from_m, _, m = b.rpartition(".")
        _temp = __import__(from_m, {}, {}, [m], -1)
        return getattr(_temp, m)
    else:
        return __import__(b, {}, {}, [], -1)


def is_userdefined(m):
    if not hasattr(m, "__file__"):
        return False
    return not any(map(m.__file__.startswith, NON_USERDEFINED_PATHES))


if __name__ == '__main__':
    for l in NON_USERDEFINED_PATHES:
        print l
