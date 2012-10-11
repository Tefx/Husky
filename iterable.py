import wrap 
import json

def dumps(variable):
    return json.dumps([wrap.dumps(item) for item in variable])

def loads(bytes):
    return [wrap.loads(item) for item in json.loads(bytes)]