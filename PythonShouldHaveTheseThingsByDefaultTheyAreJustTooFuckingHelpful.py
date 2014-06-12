#!/usr/bin/python -OO

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
## XXX THIS MODULE IS NOT ALLOWED TO IMPORT FROM OTHER MODULES IN LOLTRIS, XXX
## XXX IT IS ALLOWED TO IMPORT FROM PYTHON STDLIBS AND THIRD-PARTY LIBS    XXX
## XXX BUT NOT ANY OTHER MODULE THAT IS PART OF LOLTRIS.                   XXX
## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

class Struct(object):
    """ For those times when you really just need a symbolic namespace """
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
        return "Struct(" + "".join(["{} = {}, ".format(attr, repr(getattr(self, attr))) for attr in self.__dict__])[:-2] + ")"

    def __add__(self):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
