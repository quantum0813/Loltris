#!/usr/bin/python

## Functions that can be useful in some circumstances, but you should be careful
## about using them (think twice before using anything from here)

def contain(computation, exceptions):
    try:
        return computation()
    except exceptions:
        return None
