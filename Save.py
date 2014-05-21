#!/usr/bin/python
#-*- coding: utf-8 -*--

## =====================================================================
## Functions for saving misc. information to disk
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


from Load import IMAGEDIR, XMLDIR, MUSICDIR, DATADIR
# from lxml.etree import ElementTree
import lxml.etree as ElementTree
import os.path
import RGB
import Log

def dictsToXml(rootname, sub):
    root = ElementTree.Element(rootname)
    if type(sub).__name__ == "list":
        for d in sub:
            for key in d:
                root.append(dictsToXml(key, d[key]))
    else:
        root.text = str(sub)
    return root

def _appendScores(root, scores):
    for score in scores:
        root.append(dictsToXml("score", scores))

def saveScores(scores):
    ## Get current scores
    parser = ElementTree.XMLParser(remove_blank_text=True, encoding="utf-8")
    xml =  ElementTree.parse(os.path.join(XMLDIR, "Scores.xml"), parser)
    root = xml.getroot()

    ## Append new scores to current scores
    _appendScores(root, scores)

    ## Store the new scores along with the old ones
    xml.write(os.path.join(XMLDIR, "Scores.xml"), pretty_print=True, encoding="utf-8")

    Log.log("Saved new scores to `Scores.xml'")

def matrixToAscii(matrix, true="#", false="_", newline="\n"):
    ret = ""
    for row in matrix:
        ret += "".join([true if x else false for x in row]) + newline
    return ret

def _appendTetromino(root, color, name, matrix):
    element = ElementTree.Element("tetromino", color=RGB.rgbHexEncode(color), name=name)
    element.text = "\n" + matrixToAscii(matrix)
    root.append(element)

def saveTetromino(color, name, matrix):
    path = os.path.join(XMLDIR, "Tetrominos.xml")
    parser = ElementTree.XMLParser(encoding="utf-8")
    xml =  ElementTree.parse(path, parser)
    root = xml.getroot()

    _appendTetromino(root, color, name, matrix)

    xml.write(path)
    Log.log("Saved new tetromino to `{}'".format(path))
