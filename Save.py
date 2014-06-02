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


from Load import IMAGEDIR, MUSICDIR, DATADIR, JSONDIR, SNAPSHOTDIR, HIGHSCOREDIR, _loadText, TETROMINODIR
import os.path as Path
import json as Json
import os as OS
import RGB
import Log
import Shared
import bz2 as Bz2
import pickle as Pickle
from Globals import *

def saveScore(score, state=set()):
    try:
        with open(Path.join(HIGHSCOREDIR, "Scores.json")) as rf:
            scores = Json.load(rf)
    except (IOError, OSError):
        ## Assume that the file has been deleted, start from scratch with an empty array.
        scores = []
    seq = len(scores)
    score["date"] = Log.getTime(spec="%Y-%m-%d")
    score["time"] = Log.getTime(spec="%H:%M:%S")
    score["seq"] = seq
    scores.append(score)
    with open(Path.join(HIGHSCOREDIR, "Scores.json"), "wb") as wf:
        Json.dump(scores, wf, indent=JSON_INDENT)
    with open(Path.join(SNAPSHOTDIR, "{}.pyobj.bz2".format(seq)), "wb") as wf:
        wf.write(Bz2.compress(Pickle.dumps(state)))
    Log.log("Saved new score to `Scores.json'")

def matrixToAscii(matrix, true="#", false="_", newline="\n"):
    ret = ""
    for row in matrix:
        ret += "".join([true if x else false for x in row]) + newline
    return ret

def _appendTetromino(root, color, name, matrix):
    element = ElementTree.Element("tetromino", color=RGB.rgbHexEncode(color), name=name)
    element.text = "\n" + matrixToAscii(matrix) + "\n"
    root.append(element)

def saveOptions():
    with open(Path.join(JSONDIR, "Settings.json"), "wb") as wf:
        Json.dump(Shared.options, wf, indent=4)

def saveKeymap():
    with open(Path.join(JSONDIR, "Keymaps.json"), "wb") as wf:
        Json.dump(Shared.keymap, wf)

def _writeText(path, data):
    try:
        with open(path, "wb") as wf:
            wf.write(data)
    except (IOError, OSError):
        Log.panic("Unable to write data to `{}'".format(path))

def saveTetromino(color, name, matrix):
    _writeText(
            Path.join(TETROMINODIR, "{}.pyobj.bz2".format(name)),
            Bz2.compress(Pickle.dumps({"color": color, "matrix": matrix}))
            )

