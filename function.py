import wrap
import pickle
import types
import marshal
import pickle
import ctypes


cellnew = ctypes.pythonapi.PyCell_New
cellnew.restype = ctypes.py_object
cellnew.argtypes = (ctypes.py_object,)

def dumps(f, gen_globals=True):
    code = marshal.dumps(f. func_code)
    if f.func_closure:
        closure = [wrap.dumps(c.cell_contents) for c in f.func_closure]
    else:
        closure = None
    g = {"__builtins__": wrap.dumps(f.func_globals["__builtins__"])}
    if gen_globals:
        for item in find_requires(f):
            v = f.func_globals[item]
            g[item] = wrap.dumps(v, False)
    return pickle.dumps((code, g, closure, f.func_defaults))

def loads(bytes, use_globals=None):
    code, g, closure, defaults = pickle.loads(bytes)
    if defaults:
        defaults = tuple(defaults)
    func_code = marshal.loads(code)
    if closure:
        closure = tuple(cellnew(wrap.loads(c)) for c in closure)
    if use_globals: 
        g = use_globals
    else:
        rebuild_globals(g)
    f = types.FunctionType(func_code, g, closure=closure, argdefs=defaults)
    g[f.func_name] = f
    return f


def rebuild_globals(g):
    for name in g.iterkeys():
        g[name] = wrap.loads(g[name], g)


def find_requires(f, ignores=[]):
    rs = find_requires_code(f.func_code, f.func_globals, ignores)
    return [x for x in rs if x in f.func_globals]

def find_requires_code(code, g, ignores):
    requires = [name for name in code.co_names if name not in ignores and name != code.co_name]
    for item in code.co_consts:
        if isinstance(item, types.CodeType) and item not in ignores:
            requires += find_requires_code(item, g, ignores+requires+[code.co_name])
    i = 0
    while i<len(requires):
        item = requires[i]
        if item in g and isinstance(g[item], types.FunctionType):
            for j in find_requires(g[item], list(ignores)+requires):
                if j not in requires:
                    requires.append(j)
        i += 1
    return requires


if __name__ == '__main__':
    v = 1
    v1 = 2

    import math

    def f(x, y):
        k = 3
        return x + y + v + k

    g = lambda x: x + v

    def h(x):
        k = 2
        return lambda y: x+y+k+v1

    def k(x):
        l = h(x)
        return l(x)

    def dot(f, g):
        return lambda x:f(g(x)) 

    def n(x):
        def m(y):
            return lambda z: x+y+z+v+math.pi+id(v)+h(3)(4)
        return m

    # print find_requires(h.func_code)
    # print n.func_globals
    # print find_requires(n)
    # print n.func_globals
    # bytes = dumps(n)
    # f2 = loads(bytes)
    # print f2
    # print f2(1)
    # print f2(1)(2)
    # print f2(1)(2)(3)
    # print repr(bytes)
    # print len(bytes)

    # print len(dumps(f))

    # import snappy
    # cb = snappy.compress(dumps(find_requires))
    # print repr(cb)
    # print len(cb)

    def r(x):
        if x > 0:
            return x + r(x-1)
        else:
            return 0

    db = dumps(dumps)
    print repr(db)
    d = loads(db)
    print d
    print d(dumps) == db


