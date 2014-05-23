#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Functions that operate on matrices
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

import sys as Sys

def put(matrix, t="#", f="_"):
    """ Prints a matrix to the console for debugging purposes """
    Sys.stdout.write(" _" * len(matrix[0]))
    print
    for y in matrix:
        Sys.stdout.write("|")
        for x in y:
            Sys.stdout.write("{}|".format(t if x else f))
        print

def flip(matrix):
    """ Flips every row in a matrix (i.e it reverses each row) """
    for row in matrix:
        row.reverse()

## Because computing the next iteration is in this case better
## than storing all of them in order.
def rot90(matrix):
    """ Rotates a matrix 90 degrees clockwise """
    xl, yl = len(matrix[0]), len(matrix)

    ret = []
    plane = []
    for x in xrange(xl):
        for y in xrange(yl-1, -1, -1):
            plane.append(matrix[y][x])
        ret.append(plane)
        plane = []

    return ret

def setToMatrix(blocks, width, height):
    return[ [(x, y) in blocks for x in xrange(height)]
            for y in xrange(height)
            ]
