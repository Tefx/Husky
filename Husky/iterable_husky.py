import cPickle as pickle

import wrap


def dumps(variable, gen_globals=True):
    return pickle.dumps([wrap.dumps(item, gen_globals) for item in variable])


def loads(bytes, use_globals=False):
    return [wrap.loads(item, use_globals) for item in pickle.loads(bytes)]
