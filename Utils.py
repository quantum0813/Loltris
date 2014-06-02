#!/usr/bin/python

## Miscellaneous "utilities"

from Globals import *
import pygame as Pygame

def genKey(d):
    """
    >>> genKey({"name": "GenericFont", "size": 40, "bold": True})
    'TrueGenericFont40'
    """
    return "".join([str(d[key]) for key in sorted(d)])

def isInCube(pos, cube):
    x, y = pos
    cube_x, cube_y, cube_width, cube_height = cube
    ## Parentheses added for clarity.
    return (x > cube_x and x < cube_x+cube_width) and (y > cube_y and y < cube_y+cube_height)

def keyToString(key):
    if key == 0:
        return "(null)"
    if key == Pygame.K_SPACE:
        return "Space"

    try:
        return NONCHARACTERS.get(key, unichr(key))
    except UnicodeEncodeError:
        return "(invalid)"
