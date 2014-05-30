#!/usr/bin/python
#-*- coding: utf-8 -*-

## =====================================================================
## Functions related to loading data from disk
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

from RGB import rgbHexDecode
import os.path as Path
import Log
import json as Json
import pickle as Pickle
import bz2 as Bz2
import os as OS
from PythonShouldHaveTheseThingsByDefaultTheyAreJustTooFuckingHelpful import *

DATADIR = "data"
FONTDIR = Path.join(DATADIR, "Fonts")
IMAGEDIR = Path.join(DATADIR, "Images")
MUSICDIR = Path.join(DATADIR, "Music")
TXTDIR = Path.join(DATADIR, "TXT")
JSONDIR = Path.join(DATADIR, "JSON")
TETROMINODIR = Path.join(DATADIR, "Tetrominos")
## Not sure where this should be really
HIGHSCOREDIR = Path.join(DATADIR, "Highscores")
SNAPSHOTDIR = Path.join(HIGHSCOREDIR, "Snapshots")

def loadScores():
    path = Path.join(HIGHSCOREDIR, "Scores.json")
    Log.log("Loading scores from `{}'".format(path))
    return Json.loads(_loadText(path))

def loadHighscores(top=10):
    path = Path.join(HIGHSCOREDIR, "Scores.json")
    Log.log("Loading highscores from `{}'".format(path))
    return sorted(Json.loads(_loadText(path)), key=lambda d: d["score"], reverse=True)[:top]

def loadKeymaps():
    path = Path.join(JSONDIR, "Keymaps.json")
    Log.log("Loading keymaps from `{}'".format(path))
    return Json.loads(_loadText(path))

def _loadText(path):
    try:
        with open(path, "rb") as rf:
            return rf.read()
    except:
        Log.panic("Error while loading plain text from file `{}'".format(path))

def loadCredits():
    return _loadText(Path.join(TXTDIR, "Credits.txt"))

def loadTetrominos():
    tetrominos = []
    for filename in OS.listdir(TETROMINODIR):
        path = Path.join(TETROMINODIR, filename)
        tetromino = Pickle.loads(Bz2.decompress(_loadText(path)))
        tetrominos.append([
            tetromino["color"],
            filename.partition(".")[0],
            tetromino["matrix"],
            ])
    return tetrominos

def _loadOptions(json):
    return Json.loads(json)

def loadOptions():
    path = Path.join(JSONDIR, "Settings.json")
    return _loadOptions(_loadText(path))

def _loadSnapshot(data):
    return Pickle.loads(Bz2.decompress(data))

def loadSnapshot(seq):
    return _loadSnapshot(_loadText(Path.join(SNAPSHOTDIR, "{}.pyset.bz2".format(seq))))
