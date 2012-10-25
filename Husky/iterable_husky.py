import wrap 
import cPickle as pickle

def dumps(variable, gen_globals=True):
    return pickle.dumps([wrap.dumps(item, gen_globals) for item in variable])

def loads(bytes, use_globals=False):
    return [wrap.loads(item, use_globals) for item in pickle.loads(bytes)]