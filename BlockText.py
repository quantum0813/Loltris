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

_ = False
O = True

STANDARD_FONT = {
        "A": [[O,O,O],
              [O,_,O],
              [O,O,O],
              [O,_,O],
              [O,_,O]],

        "B": [[O,O,_],
              [O,_,O],
              [O,O,_],
              [O,_,O],
              [O,O,_]],

        "C": [[O,O,O],
              [O,_,_],
              [O,_,_],
              [O,_,_],
              [O,O,O]],

        "D": [[O,O,_],
              [O,_,O],
              [O,_,O],
              [O,_,O],
              [O,O,_]],

        "E": [[O,O,O],
              [O,_,_],
              [O,O,O],
              [O,_,_],
              [O,O,O]],

        "F": [[O,O,O],
              [O,_,_],
              [O,O,O],
              [O,_,_],
              [O,_,_]],

        "G": [[O,O,O],
              [O,_,_],
              [O,_,_],
              [O,_,O],
              [O,O,O]],

        "H": [[O,_,O],
              [O,_,O],
              [O,O,O],
              [O,_,O],
              [O,_,O]],

        "I": [[O],
              [O],
              [O],
              [O],
              [O]],

        "J": [[_,_,O],
              [_,_,O],
              [_,_,O],
              [O,_,O],
              [_,O,O]],

        "K": [[O,_,O],
              [O,_,O],
              [O,O,_],
              [O,_,O],
              [O,_,O]],

        "L": [[O,_,_],
              [O,_,_],
              [O,_,_],
              [O,_,_],
              [O,O,O]],

        "M": [[O,_,O],
              [O,O,O],
              [O,_,O],
              [O,_,O],
              [O,_,O]],

        "N": [[O,_,_,O],
              [O,O,_,O],
              [O,_,O,O],
              [O,_,_,O],
              [O,_,_,O]],

        "O": [[O,O,O],
              [O,_,O],
              [O,_,O],
              [O,_,O],
              [O,O,O]],

        "P": [[O,O,O],
              [O,_,O],
              [O,O,O],
              [O,_,_],
              [O,_,_]],

        "Q": [[O,O,O,O],
              [O,_,_,O],
              [O,_,_,O],
              [O,_,O,O],
              [O,O,O,_]],

        "R": [[O,O,O],
              [O,_,O],
              [O,O,_],
              [O,_,O],
              [O,_,O]],

        "S": [[O,O,O],
              [O,_,_],
              [_,O,_],
              [_,_,O],
              [O,O,O]],

        "T": [[O,O,O],
              [_,O,_],
              [_,O,_],
              [_,O,_],
              [_,O,_]],

        "U": [[O,_,O],
              [O,_,O],
              [O,_,O],
              [O,_,O],
              [O,O,O]],

        "V": [[O,_,O],
              [O,_,O],
              [O,_,O],
              [O,_,O],
              [_,O,_]],

        "W": [[O,_,O,_,O],
              [O,_,O,_,O],
              [O,_,O,_,O],
              [O,_,O,_,O],
              [_,O,_,O,_]],

        "X": [[O,_,O],
              [O,_,O],
              [_,O,_],
              [O,_,O],
              [O,_,O]],

        "Y": [[O,_,O],
              [O,_,O],
              [_,O,_],
              [_,O,_],
              [_,O,_]],

        "Z": [[O,O,O],
              [_,_,O],
              [_,O,_],
              [O,_,_],
              [O,O,O]],

        " ": [[_],
              [_],
              [_],
              [_],
              [_]],
        }

def getChar(char, font):
    if char.islower() and not font.get(char):
        return font.get(char.upper())
    if char.isupper() and not font.get(char):
        return font.get(char.lower())
    return font[char]

def render(text, font, spaces=1, padding=False):
    rows = len(getChar("a", font))
    matrix = [[] for _ in xrange(rows)]
    if spaces:
        spacer = [[False for _ in xrange(spaces)] for _ in xrange(rows)]
    last = len(text); i = 0
    if padding:
        Matrix.append(matrix, spacer)
    for char in text:
        i += 1
        letter_matrix = getChar(char, font)
        print(letter_matrix)
        Matrix.append(matrix, letter_matrix)
        if spaces and (i != last or padding):
            Matrix.append(matrix, spacer)
    return matrix

if __name__ == '__main__':
    Matrix.put(render("woot", STANDARD_FONT))
