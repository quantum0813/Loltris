#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Write text in block letters, this kind of text can be put inside
## a Jobs.Board
##
## Copyright (C) 2014 Jonas Møller <jonasmo441@gmail.com>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
## =====================================================================

import Matrix
import Log
import struct
import Load
from math import ceil

def getChar(char, font):
    if char.islower() and char not in font:#font.get(char):
        return font.get(char.upper())
    if char.isupper() and char not in font:#font.get(char):
        return font.get(char.lower())

    if font.get(char):
        return font[char]
    else:
        return font["invalid"]

def render(text, font, spaces=1, padding=False):
    """
    Using a bitmap font represented as a 2d matrix, and some text
    represented as an ASCII string a new matrix is returned. This
    matrix contains the rendered blocktext.

    >>> Log.LOGLEVEL = 0
    >>> Matrix.put(render("TEST", Load.loadBlockFont("standard"))
     _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    |#|#|#|_|#|#|#|_|#|#|#|_|#|#|#|
    |_|#|_|_|#|_|_|_|#|_|_|_|_|#|_|
    |_|#|_|_|#|#|#|_|_|#|_|_|_|#|_|
    |_|#|_|_|#|_|_|_|_|_|#|_|_|#|_|
    |_|#|_|_|#|#|#|_|#|#|#|_|_|#|_|
    """
    Log.debug("Rendering blocktext {}".format(repr(text)))
    rows = len(getChar("invalid", font))
    matrix = [[] for _ in xrange(rows)]
    if spaces:
        spacer = [[False for _ in xrange(spaces)] for _ in xrange(rows)]
    last = len(text); i = 0
    if padding:
        Matrix.append(matrix, spacer)
    for char in text:
        i += 1
        letter_matrix = getChar(char, font)
        Matrix.append(matrix, letter_matrix)
        if spaces and (i != last or padding):
            Matrix.append(matrix, spacer)
    return matrix

if __name__ == '__main__':
    import doctest
    doctest.testmod()
