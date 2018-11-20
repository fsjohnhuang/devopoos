import re


def complement(f):
    return lambda *args: not f(*args)


def rfind(r):
    return lambda s: re.search(r, s)


def always(a):
    return lambda _: a


T = always(True)
F = always(False)
