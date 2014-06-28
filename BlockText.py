#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Write text in block letters, this kind of text can be put inside
## a Jobs.Board
##
## Copyright (C) 2014 Jonas Møller <shrubber@tfwno.gf>
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
from math import ceil

_ = 0

STANDARD_FONT = {
        "A": [[1,1,1],
              [1,_,1],
              [1,1,1],
              [1,_,1],
              [1,_,1]],

        "B": [[1,1,_],
              [1,_,1],
              [1,1,_],
              [1,_,1],
              [1,1,_]],

        "C": [[1,1,1],
              [1,_,_],
              [1,_,_],
              [1,_,_],
              [1,1,1]],

        "D": [[1,1,_],
              [1,_,1],
              [1,_,1],
              [1,_,1],
              [1,1,_]],

        "E": [[1,1,1],
              [1,_,_],
              [1,1,1],
              [1,_,_],
              [1,1,1]],

        "F": [[1,1,1],
              [1,_,_],
              [1,1,1],
              [1,_,_],
              [1,_,_]],

        "G": [[1,1,1],
              [1,_,_],
              [1,_,_],
              [1,_,1],
              [1,1,1]],

        "H": [[1,_,1],
              [1,_,1],
              [1,1,1],
              [1,_,1],
              [1,_,1]],

        "I": [[1],
              [1],
              [1],
              [1],
              [1]],

        "J": [[_,_,1],
              [_,_,1],
              [_,_,1],
              [1,_,1],
              [_,1,1]],

        "K": [[1,_,1],
              [1,_,1],
              [1,1,_],
              [1,_,1],
              [1,_,1]],

        "L": [[1,_,_],
              [1,_,_],
              [1,_,_],
              [1,_,_],
              [1,1,1]],

        "M": [[1,_,1],
              [1,1,1],
              [1,_,1],
              [1,_,1],
              [1,_,1]],

        "N": [[1,_,_,1],
              [1,1,_,1],
              [1,_,1,1],
              [1,_,_,1],
              [1,_,_,1]],

        "O": [[1,1,1],
              [1,_,1],
              [1,_,1],
              [1,_,1],
              [1,1,1]],

        "P": [[1,1,1],
              [1,_,1],
              [1,1,1],
              [1,_,_],
              [1,_,_]],

        "Q": [[1,1,1,1],
              [1,_,_,1],
              [1,_,_,1],
              [1,_,1,1],
              [1,1,1,_]],

        "R": [[1,1,1],
              [1,_,1],
              [1,1,_],
              [1,_,1],
              [1,_,1]],

        "S": [[1,1,1],
              [1,_,_],
              [_,1,_],
              [_,_,1],
              [1,1,1]],

        "T": [[1,1,1],
              [_,1,_],
              [_,1,_],
              [_,1,_],
              [_,1,_]],

        "U": [[1,_,1],
              [1,_,1],
              [1,_,1],
              [1,_,1],
              [1,1,1]],

        "V": [[1,_,1],
              [1,_,1],
              [1,_,1],
              [1,_,1],
              [_,1,_]],

        "W": [[1,_,1,_,1],
              [1,_,1,_,1],
              [1,_,1,_,1],
              [1,_,1,_,1],
              [_,1,_,1,_]],

        "X": [[1,_,1],
              [1,_,1],
              [_,1,_],
              [1,_,1],
              [1,_,1]],

        "Y": [[1,_,1],
              [1,_,1],
              [_,1,_],
              [_,1,_],
              [_,1,_]],

        "Z": [[1,1,1],
              [_,_,1],
              [_,1,_],
              [1,_,_],
              [1,1,1]],

        "1": [[_,1,_],
              [1,1,_],
              [_,1,_],
              [_,1,_],
              [1,1,1]],

        "2": [[_,1,_],
              [1,_,1],
              [_,_,1],
              [_,1,_],
              [1,1,1]],

        "3": [[1,1,_],
              [_,_,1],
              [_,1,_],
              [_,_,1],
              [1,1,_]],

        "4": [[1,_,1],
              [1,_,1],
              [1,1,1],
              [_,_,1],
              [_,_,1]],

        "5": [[1,1,1],
              [1,_,_],
              [_,1,1],
              [_,_,1],
              [1,1,_]],

        "6": [[_,1,1],
              [1,_,_],
              [1,1,_],
              [1,_,1],
              [_,1,_]],

        "7": [[1,1,1],
              [_,_,1],
              [_,1,_],
              [_,1,_],
              [_,1,_]],

        "8": [[1,1,1],
              [1,_,1],
              [_,1,_],
              [1,_,1],
              [1,1,1]],

        "9": [[_,1,_],
              [1,_,1],
              [_,1,1],
              [_,_,1],
              [_,_,1]],

        "+": [[_,_,_],
              [_,1,_],
              [1,1,1],
              [_,1,_],
              [_,_,_]],

        "-": [[_,_,_],
              [_,_,_],
              [1,1,1],
              [_,_,_],
              [_,_,_]],

        "_": [[_,_,_],
              [_,_,_],
              [_,_,_],
              [_,_,_],
              [1,1,1]],

        ";": [[_,_,_],
              [_,1,_],
              [_,_,_],
              [_,1,_],
              [1,_,_]],

        "!": [[1],
              [1],
              [1],
              [_],
              [1]],

        ".": [[_],
              [_],
              [_],
              [_],
              [1]],

        ":": [[_],
              [1],
              [_],
              [1],
              [_]],

        "/": [[_,_,1],
              [_,_,1],
              [_,1,_],
              [1,_,_],
              [1,_,_]],

        "\\": [[1,_,_],
               [1,_,_],
               [_,1,_],
               [_,_,1],
               [_,_,1]],

        "?": [[1,1,1],
              [_,_,1],
              [_,1,_],
              [_,_,_],
              [_,1,_]],

        "(": [[_,1],
              [1,_],
              [1,_],
              [1,_],
              [_,1]],

        ")": [[1,_],
              [_,1],
              [_,1],
              [_,1],
              [1,_]],

        "]": [[1,1],
              [_,1],
              [_,1],
              [_,1],
              [1,1]],

        "[": [[1,1],
              [1,_],
              [1,_],
              [1,_],
              [1,1]],

        "*": [[1,_,_,1],
              [_,1,1,_],
              [_,1,1,_],
              [1,_,_,1],
              [_,_,_,_]],

        "*": [[_,1,_],
              [1,_,1],
              [_,_,_],
              [_,_,_],
              [_,_,_]],

        "|": [[1],
              [1],
              [1],
              [1],
              [1]],

        '"': [[1,_,1],
              [1,_,1],
              [_,_,_],
              [_,_,_],
              [_,_,_]],

        "'": [[1],
              [1],
              [_],
              [_],
              [_]],

        "=": [[_,_,_],
              [1,1,1],
              [_,_,_],
              [1,1,1],
              [_,_,_]],

        " ": [[_],
              [_],
              [_],
              [_],
              [_]],

        "#": [[_,1,_,1,_],
              [1,1,1,1,1],
              [_,1,_,1,_],
              [1,1,1,1,1],
              [_,1,_,1,_]],

        "invalid": [[1,1,1],
                    [_,1,_],
                    [1,_,1],
                    [_,1,_],
                    [1,1,1]],

        }

def getChar(char, font):
    if char.islower() and not font.get(char):
        return font.get(char.upper())
    if char.isupper() and not font.get(char):
        return font.get(char.lower())

    if font.get(char):
        return font[char]
    else:
        return font["invalid"]

def render(text, font, spaces=1, padding=False):
    """
    >>> Matrix.put(render("TEST", STANDARD_FONT))
     _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    |#|#|#|_|#|#|#|_|#|#|#|_|#|#|#|
    |_|#|_|_|#|_|_|_|#|_|_|_|_|#|_|
    |_|#|_|_|#|#|#|_|_|#|_|_|_|#|_|
    |_|#|_|_|#|_|_|_|_|_|#|_|_|#|_|
    |_|#|_|_|#|#|#|_|#|#|#|_|_|#|_|
    """
    Log.debug("Rendering blocktext: {}".format(repr(text)))
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

"""
Filename: standard.sbf
<<<
[rows (4)]

[character-name-length (1)][character-name (...)]
[bytes per row (4)]
[row (row-length)]...
>>>
"""

## Note that these masks will be reversed
def listToMasks(xs):
    assert xs, "List must contain at least one item"

    masks = [0 for _ in xrange(int(ceil(len(xs) / 32.0)))]
    i = 0
    pos = 0
    for x in xs:
        if x:
            masks[pos] = masks[pos] | (1 << i)
        i += 1
        if i == 32:
            i = 0
            pos += 1
    return masks

def dumpFont(font):
    buf = ""
    buf += struct.pack("<I", len(getChar("invalid", font)))

    for charname in font:
        assert len(charname) < 255, "Character name must be under 255 characters long"

        buf += struct.pack("B", len(charname)) + charname ## Charname-length + charname
        buf += struct.pack("<I", len(font[charname][0])) ## Length of a single row in blocks, in bits
        for row in font[charname]:
            for mask in listToMasks(row):
                buf += struct.pack("<I", mask)

    return buf

def loadFontStream(handle):
    rows = struct.unpack("<I", handle.read(4))
    
    while True:
        charname_length = struct.unpack("B", handle.read(1))
        charname = handle.read(charname_length)
        row_length = struct.unpack("<I", handle.read(4))
        row_byte_length = ceil(row_length / 32.0)
        row_bytes = []
        for i in xrange(row_length):
            row_bytes.append(handle.read(row_byte_length))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
