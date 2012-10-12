import wrap
import pickle


def dumps(variable):
    return pickle.dumps({wrap.dumps(k):wrap.dumps(v) for k,v in variable.iteritems()})

def loads(bytes):
    return {wrap.loads(k):wrap.loads(v) for k,v in pickle.loads(bytes).iteritems()}