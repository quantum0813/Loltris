#!/usr/bin/python -OO

## PSHTTBDTAJTFH
## Python-Should-Have-These-Things-By-Default-They-Are-Just-Too-Fucking-Helpful

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
## XXX THIS MODULE IS NOT ALLOWED TO IMPORT FROM OTHER MODULES IN LOLTRIS, XXX
## XXX IT IS ALLOWED TO IMPORT FROM PYTHON STDLIBS AND THIRD-PARTY LIBS    XXX
## XXX BUT NOT ANY OTHER MODULE THAT IS PART OF LOLTRIS.                   XXX
## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

## Copy should be a built-in
from copy import copy

class Struct(object):
    """ For those times when you really just need a symbolic namespace 

        >inb4 using classes as hash tables is always bad

        As syntax goes:
            namespace.value > hashtable["value"]
    """
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __str__(self):
        """
        >>> c = Struct(arg0=0, arg1=1)
        >>> c.arg2 = "value"
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
