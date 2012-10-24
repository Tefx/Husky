def dumps(m):
    return m.__name__

def loads(b):
    return __import__(b, {}, {}, -1)