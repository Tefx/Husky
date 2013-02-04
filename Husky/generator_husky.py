import wrap


def gen(x):
    for i in xrange(x):
        yield i

g = gen(10)

if __name__ == '__main__':
    print g.next()
    print g.next()

    # print vars(g)
    # bytes = wrap.dumps(g)
    # print g.next()
    # g2 = wrap.loads(bytes)
    # print g2.next()

    import types
    # print help(types.GeneratorType)
    print type(g)
