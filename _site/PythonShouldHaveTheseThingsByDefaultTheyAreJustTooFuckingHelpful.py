#!/usr/bin/python

class Struct(object):
    """ For those times when you really just need a symbolic namespace """
    def __init__(self, *args, **kwargs):
        for arg in args:
            setattr(self, arg, None)
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

