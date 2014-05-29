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


from Load import IMAGEDIR, XMLDIR, MUSICDIR, DATADIR, JSONDIR, SNAPSHOTDIR, HIGHSCOREDIR, _loadText
# import lxml.etree as ElementTree
from xml.etree import ElementTree
import os.path as Path
import json as Json
import os as OS
import RGB
import Log
import Shared
import bz2 as Bz2
import pickle as Pickle

def dictToXml(rootname, sub):
    root = ElementTree.Element(rootname)
    if type(sub).__name__ == "dict":
        for d in sub:
            root.append(dictToXml(d, sub[d]))
    else:
        root.text = str(sub)
    return root

def dictsToXml(rootname, sub):
    root = ElementTree.Element(rootname)
    if type(sub).__name__ == "list":
        for d in sub:
            for key in d:
                root.append(dictsToXml(key, d[key]))
    else:
        root.text = unicode(sub)
    return root

def saveScore(score, state=set()):
    try:
        with open(Path.join(HIGHSCOREDIR, "Scores.json")) as rf:
            scores = Json.load(rf)
    except (IOError, OSError):
        ## File does not exist yet
        scores = []
    score["date"] = Log.getTime(spec="%Y:%m:%d")
    scores.append(score)
    with open(Path.join(HIGHSCOREDIR, "Scores.json"), "w") as wf:
        Json.dump(scores, wf, indent=JSON_INDENT)
    Log.log("Saved new score to `Scores.json'")

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
    path = Path.join(XMLDIR, "Tetrominos.xml")
    parser = ElementTree.XMLParser(encoding="utf-8")
    xml =  ElementTree.parse(path, parser)
    root = xml

    _appendTetromino(root, color, name, matrix)

    with open(path, "w") as wf:
        wf.write(ElementTree.tostring(xml))
    Log.log("Saved new tetromino to `{}'".format(path))

def saveOptions():
    with open(Path.join(JSONDIR, "Settings.json"), "w") as wf:
        Json.dump(Shared.options, wf, indent=4)

def saveKeymap():
    with open(Path.join(JSONDIR, "Keymaps.json"), "w") as wf:
        Json.dump(Shared.keymap, wf)
