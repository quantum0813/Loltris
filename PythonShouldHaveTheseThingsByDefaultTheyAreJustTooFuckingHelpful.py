#!/usr/bin/python

class Struct(object):
    """ For those times when you really just need a symbolic namespace """
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __str__(self):
        return "Struct(" + "".join(["{} = {}, ".format(attr, getattr(self, attr)) for attr in self.__dict__])[:-2] + ")"

    def __add__(self):
        pass
