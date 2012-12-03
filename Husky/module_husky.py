import os
import sys
from distutils import sysconfig

NON_USERDEFINED_PATHES = [
    sysconfig.get_python_lib(standard_lib=True, prefix=os.path.realpath(sys.prefix)),
    sysconfig.get_python_lib(standard_lib=True),
    sysconfig.get_python_lib(standard_lib=False)
]

def dumps(m):
    return m.__name__

def loads(b):
    return __import__(b, {}, {}, -1)

def is_userdefined(m):
    if not hasattr(m, "__file__"):
        return False
    return not any(map(m.__file__.startswith, NON_USERDEFINED_PATHES))