#!/usr/bin/python -OO
#-*- coding: utf-8 -*-

## PSHTTBDTAJTFH
## Python-Should-Have-These-Things-By-Default-They-Are-Just-Too-Fucking-Helpful

## Written by Jonas Møller
## Public domain

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
## XXX THIS MODULE IS NOT ALLOWED TO IMPORT FROM OTHER MODULES IN LOLTRIS, XXX
## XXX IT IS ALLOWED TO IMPORT FROM PYTHON STDLIBS AND THIRD-PARTY LIBS    XXX
## XXX BUT NOT ANY OTHER MODULE THAT IS PART OF LOLTRIS.                   XXX
## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

## Copy should be a built-in
from copy import copy

from pprint import pprint

class Struct(object):
    """ Basically a hash table, but a struct allows for accessing attributes like this:
        struct.attribute

        Attributes can still be accessed as such:
        struct["attribute"]
    """
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __str__(self):
        """
        >>> c = Struct(arg0=0, arg1=1)
        >>> c.arg2 = "value"
        >>> topkek
        >>> str(c)
        "Struct(arg0 = 0, arg1 = 1, arg2 = 'value')"
        """
        ## Yup.
        return "Struct(" + "".join(["{} = {}, ".format(attr, repr(getattr(self, attr))) for attr in self.__dict__])[:-2] + ")"

    def __len__(self):
        return len(self.__dict__)

    def __add__(self, obj):
        if isinstance(obj, dict):
            obj = Struct(**obj)

        if isinstance(obj, Struct):
            data = self.__dict__.copy()
            data.update(obj.__dict__)
            return Struct(**data)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(obj)))

    def __contains__(self, obj):
        return obj in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
