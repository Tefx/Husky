import wrap
import json

def dumps(variable):
    return json.dumps({wrap.dumps(k):wrap.dumps(v) for k,v in variable.iteritems()})

def loads(bytes):
    return {wrap.loads(k):wrap.loads(v) for k,v in json.loads(bytes).iteritems()}