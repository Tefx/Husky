import wrap
import json
import types
import marshal
import pickle
import ctypes

cellnew = ctypes.pythonapi.PyCell_New
cellnew.restype = ctypes.py_object
cellnew.argtypes = (ctypes.py_object,)

def dumps(f):
    code = marshal.dumps(f.func_code)
    if f.func_closure:
        closure = [wrap.dumps(c.cell_contents) for c in f.func_closure]
    else:
        closure = None
    return json.dumps((code, closure))

def loads(bytes):
    code, closure = json.loads(bytes)
    func_code = marshal.loads(code)
    if closure:
        closure = tuple(cellnew(wrap.loads(c)) for c in closure)
    return  types.FunctionType(func_code, {}, closure=closure)

