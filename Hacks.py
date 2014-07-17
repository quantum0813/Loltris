#!/usr/bin/python

def contain(computation, exceptions):
    try:
        return computation()
    except exceptions:
        return None

def chain():
    def chain(function, *args, **kwargs):
        """
        >>> import sys
        >>> f = lambda: chain()
        """
        function(*args, **kwargs)
        return True
