Husky
=====

An Advanced serializing library for python, like pickle, but can dump more, for example, functions.

# Install
    
    $ pip install Husky


# Usage
    
    def foo():
        return bar()
        
    def bar():
        return "ok"
    
    bytes = dumps(a)
    f = loads(a)
    
    f()