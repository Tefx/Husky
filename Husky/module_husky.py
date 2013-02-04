import os
import sys
from distutils import sysconfig
import site

NON_USERDEFINED_PATHES = [
    sysconfig.get_python_lib(standard_lib=True, prefix=os.path.realpath(sys.prefix)),
    sysconfig.get_python_lib(standard_lib=True),
] + site.getsitepackages()

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
    for l in  NON_USERDEFINED_PATHES:
        print l
