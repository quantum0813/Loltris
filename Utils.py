#!/usr/bin/python

## Miscellaneous "utilities" that didn't fit into any other particular module

from Globals import *
import pygame as Pygame

## Generate a key for a dictionary, used for storing fonts but can be used
## to store anything represented as a constant dictionary.
def genKey(d):
    """
    >>> genKey({"name": "GenericFont", "size": 40, "bold": True})
    'TrueGenericFont40'
    """
    return "".join([str(d[key]) for key in sorted(d)])

## Check if coordinates pos is within cube
def isInCube(pos, cube):
    """
    >>> isInCube((10, 10), (5, 5, 15, 15))
    True
    """
    x, y = pos
    cube_x, cube_y, cube_width, cube_height = cube
    ## Parentheses added for clarity.
    return (x > cube_x and x < cube_x+cube_width) and (y > cube_y and y < cube_y+cube_height)

def keyToString(key):
    """
    >>> keyToString(K_LALT)
    u'L-Alt'
    >>> keyToString(0x31)
    u'1'
    """
    try:
        return NONCHARACTERS.get(key, unichr(key))
    except UnicodeEncodeError:
        return "(invalid)"

if __name__ == '__main__':
    import doctest
    doctest.testmod()
