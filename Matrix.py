#!/usr/bin/python

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
    for row in matrix:
        row.reverse()

## Because computing the next iteration is in this case better
## than storing all of them in order.
def rot90(matrix):
    xl, yl = len(matrix[0]), len(matrix)

    ret = []
    plane = []
    for x in xrange(xl):
        for y in xrange(yl-1, -1, -1):
            plane.append(matrix[y][x])
        ret.append(plane)
        plane = []

    return ret
