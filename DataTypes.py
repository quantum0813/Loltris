#!/usr/bin/python -OO
#-*- coding: utf-8 -*-

## Helpful general purpose datatypes

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
## XXX THIS MODULE IS NOT ALLOWED TO IMPORT FROM OTHER MODULES IN LOLTRIS, XXX
## XXX IT IS ALLOWED TO IMPORT FROM PYTHON STDLIBS AND THIRD-PARTY LIBS    XXX
## XXX BUT NOT ANY OTHER MODULE THAT IS PART OF LOLTRIS.                   XXX
## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

from copy import copy

class Struct(object):
    """ Basically a hash table, but a Struct allows for accessing attributes like this:
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

class BiDict(object):
    """ Bi-directional dictionary

    >>> b = BiDict({"a": 1, "b": 2, "c": 3})
    >>> b["a"]
    1
    >>> b[1]
    'a'
    >>> b["c"] = 4
    >>> b[4]
    'c'
    >>> b[3]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "DataTypes.py", line 104, in __getitem__
        return self._dict_b[key]
    KeyError: 3
    >>> str(b)
    "{'a' <=> 1, 'c' <=> 4, 'b' <=> 2}"
    >>> del b["b"]
    >>> str(b)
    "{'a' <=> 1, 'c' <=> 4}"
    >>> 
    """
    def __init__(self, **kwargs):
        if not kwargs:
            raise TypeError("Will not create BiDict from empty kwargs state")

        akey = kwargs.keys()[0]
        self._type_a = type(akey)
        self._type_b = type(kwargs[akey])
        if self._type_a == self._type_b:
            raise TypeError("Keys are of the same type as values")

        self._dict_a = copy(kwargs)
        self._dict_b = {}

        for key in kwargs:
            if not isinstance(key, self._type_a):
                raise TypeError("Keys are of different types")
            if not isinstance(kwargs[key], self._type_b):
                raise TypeError("Values are of different types")
            self._dict_b[kwargs[key]] = key

    def __getitem__(self, key):
        if isinstance(key, self._type_a):
            return self._dict_a[key]
        if isinstance(key, self._type_b):
            return self._dict_b[key]

    def __setitem__(self, key, value):
        if isinstance(key, self._type_a):
            del self[key]
            self._dict_a[key] = value
            self._dict_b[value] = key
        if isinstance(key, self._type_b):
            del self[key]
            self._dict_b[key] = value
            self._dict_a[value] = key

    def __delitem__(self, key):
        if isinstance(key, self._type_a):
            del self._dict_b[self._dict_a[key]]
            del self._dict_a[key]
        if isinstance(key, self._type_b):
            del self._dict_a[self._dict_b[key]]
            del self._dict_b[key]

    def __str__(self):
        return "{" + ", ".join(["{!r} <=> {!r}".format(key, self[key]) for key in self._dict_a]) + "}"

    def __contains__(self, obj):
        return obj in self._dict_a or obj in self._dict_b

    def get(self, key, *args):
        alternative = None
        if args:
            alternative = args[0]
        if key in self:
            return self[key]
        else:
            return alternative

    def __iter__(self):
        return iter(self._dict_a)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
