import types
import struct
import json
import pickle
import iterable
import dictionary
import function


dispatches = [
    (types.NoneType, json),
    (types.BooleanType, json),
    (types.IntType, json),
    (types.LongType, json),
    (types.FloatType, json),
    (types.StringType, json),
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
]


def tag(s, t):
    return struct.pack(">c", chr(dispatches.index(t)))+s

def untag(s):
    return ord(struct.unpack(">c", s)[0])

def dumps(d):
    for item in dispatches:
        if isinstance(d, item[0]):
            return tag(item[1].dumps(d), item)
    return None

def loads(s):
    t, m = dispatches[untag(s[0])]
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