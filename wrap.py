import types
import struct
import pickle
import iterable
import dictionary
import function
import module
import snappy as ziplib


def compressed(f):
    return lambda *args: ziplib.compress(pickle.dumps(f(*args)))

def decompressed(f):
    return lambda x, *args: f(pickle.loads(ziplib.decompress(x)), *args)

dispatches = [
    (types.NoneType, pickle),
    (types.BooleanType, pickle),
    (types.IntType, pickle),
    (types.LongType, pickle),
    (types.FloatType, pickle),
    (types.StringType, pickle),
    (types.ComplexType, pickle),
    (types.UnicodeType, pickle),
    (types.BuiltinFunctionType, pickle),
    (types.XRangeType, pickle),
    (types.TupleType, iterable),
    (types.ListType, iterable),
    (types.GeneratorType, iterable),
    (types.DictType, dictionary),
    (types.DictionaryType, dictionary),
    (types.FunctionType, function),
    (types.LambdaType, function),
    (types.ModuleType, module),
    (object, pickle)
]


def tag(s, t):
    return struct.pack(">c", chr(dispatches.index(t)))+s

def untag(s):
    return ord(struct.unpack(">c", s)[0])

@compressed
def dumps(d, gen_globals=True):
    for item in dispatches:
        if isinstance(d, item[0]):
            if item[1] == function:
                return tag(item[1].dumps(d, gen_globals), item)
            else:
                return tag(item[1].dumps(d), item)
    return None

@decompressed
def loads(s, use_globals=None):
    t, m = dispatches[untag(s[0])]
    if m == function:
        f = m.loads(s[1:], use_globals)
    else:
        f = m.loads(s[1:])
    if not isinstance(f, t):
        f = t(f)
    return f

if __name__ == '__main__':
    v = {1:[1,2,3], "v":None}
    b = dumps(v)
    print repr(b)
    v1 = loads(b)
    print v1