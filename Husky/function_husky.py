import wrap
import cPickle as pickle
import types
import marshal
import ctypes


cellnew = ctypes.pythonapi.PyCell_New
cellnew.restype = ctypes.py_object
cellnew.argtypes = (ctypes.py_object,)

def dumps(f, gen_globals=True):
    code = marshal.dumps(f.func_code)
    if f.func_closure:
        closure = [c.cell_contents for c in f.func_closure]
    else:
        closure = None
    g = {}
    if gen_globals:
        for item in find_requires(f):
            g[item] = f.func_globals[item]
    return wrap.dumps((code, g, closure, f.func_defaults), False)

def loads(bytes, use_globals=False):
    code, g, closure, defaults = wrap.loads(bytes, True)
    g["__builtins__"] = __import__("__builtin__")
    if defaults:
        defaults = tuple(defaults)
    func_code = marshal.loads(code) 
    if closure:
        closure = tuple(cellnew(c) for c in closure)
    f = types.FunctionType(func_code, g, closure=closure, argdefs=defaults)
    if not use_globals:
        for n,f0 in f.func_globals.iteritems():
            if isinstance(f0, types.FunctionType):
                f.func_globals[n] = replace_globals(f0, f.func_globals)
        g[f.func_name] = f
    return f

def replace_globals(f, g):
    return types.FunctionType(f.func_code, g, f.func_closure, f.func_defaults)

def find_requires(f, ignores=["__builtins__"]):
    # print "f", f.__module__
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
        # if item in g and hasattr(g[item], "__module__"):
            # print item, g[item].__module__
        if item in g and isinstance(g[item], types.FunctionType):
            for k,v in g[item].func_globals.iteritems():
                g[k] = v
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
    # print db
    # d = loads(db)
    # print d
    # print d(dumps) == db
    # print type(db)

    import json
    import snappy

    bb = snappy.compress(json.dumps(db))
    print bb
    print type(bb)
    bbb = json.loads(snappy.decompress(bb))
    print type(bbb)
    print loads(bbb.encode())

