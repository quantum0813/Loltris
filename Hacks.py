#!/usr/bin/python

## Some hacks

def contain(computation, exceptions):
    try:
        return computation()
    except exceptions:
        return None

def chain(f, *fs):
    return (lambda: (lambda: f() or True)() and chain(*fs)()) if fs else f
