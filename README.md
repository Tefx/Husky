Husky
=====

An Advanced serializing library like pickle but can dump more, for example, functions.

# Usage
    
    def foo():
        return bar()
        
    def bar():
        return "ok"
    
    bytes = dumps(a)
    f = loads(a)
    
    f()