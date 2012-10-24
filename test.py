from Husky import dumps, loads, function
import math
import types
import pickle
import marshal
import Husky

def f(x, y):
    return x+y

def g(x):
    return lambda y: x+y

def d(f):
    return dumps(f)

b = dumps(d)
print len(b)
print repr(b)
