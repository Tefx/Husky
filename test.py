from wrap import dumps, loads


def f(x, y):
    return x+y

def g(x):
    return lambda y: x+y


if __name__ == '__main__':
    # b = dumps(f)
    # print repr(b)

    # f0 = loads(b)
    # print f0
    # print f0(1,3)

    # ff = g(1)
    # b = dumps(ff)
    # print repr(b)
    # f0 = loads(b)
    # print f0
    # print f0(2)

    def r(x):
        if x > 0:
            return x + r(x-1)
        else:
            return 0

    b = dumps(r)
    print loads(b)(10)