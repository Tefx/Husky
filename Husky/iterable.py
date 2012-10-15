import wrap 
import cPickle as pickle

def dumps(variable):
    return pickle.dumps([wrap.dumps(item) for item in variable])

def loads(bytes):
    return [wrap.loads(item) for item in pickle.loads(bytes)]