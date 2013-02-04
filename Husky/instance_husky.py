import wrap
import types


def dumps(ins):
    d = getattr(ins, "__dict__", None)
    return wrap.dumps((ins.__class__, d))

def loads(bytes):
    C, d = wrap.loads(bytes)
    ins = C.__new__(C)
    if d:
        if not hasattr(ins, "__dict__"):
            ins.__dict__ = {}
        ins.__dict__.update(d)
    return ins


if __name__ == '__main__':
    class UserClass(object):
        def __init__(self, a):
            self.a = a

        def foo(self, x):
            return self.a + x

    c = UserClass(1)
    bytes = dumps(c)
    c2 = loads(bytes)
    print bytes