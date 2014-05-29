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

from xml.etree import ElementTree
from RGB import rgbHexDecode
import os.path as Path
import Log
import json as Json
import pickle as Pickle
import bz2 as Bz2

DATADIR = "data"
FONTDIR = Path.join(DATADIR, "Fonts")
XMLDIR = Path.join(DATADIR, "XML")
IMAGEDIR = Path.join(DATADIR, "Images")
MUSICDIR = Path.join(DATADIR, "Music")
TXTDIR = Path.join(DATADIR, "TXT")
JSONDIR = Path.join(DATADIR, "JSON")
## Not sure where this should be really
HIGHSCOREDIR = Path.join(DATADIR, "Highscores")
SNAPSHOTDIR = Path.join(HIGHSCOREDIR, "Snapshots")

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
        with open(path) as rf:
            return rf.read()
    except:
        Log.panic("Error while loading plain text from file `{}'".format(path))

def loadCredits():
    return _loadText(Path.join(TXTDIR, "Credits.txt"))

def _loadTetrominos(xml, verbose=True):
    tree = ElementTree.XML(xml)
    tree_items = dict(tree.items())

    def makeTetromino(text):
        for chars in filter(bool, (l.strip(" ") for l in text.splitlines())):
            line = []
            for char in chars:
                if char == tree_items["true"]:
                    line.append(1)
                elif char == tree_items["false"]:
                    line.append(0)
            yield line

    tetrominos = []
    for sub in tree.getchildren():
        sub_items = dict(sub.items())
        if verbose:
            Log.log("Loading tetromino `{}' with color `{}'".format(sub_items["name"], sub_items["color"]))
        tetrominos.append([
                rgbHexDecode(sub_items["color"]),
                sub_items["name"],
                list(makeTetromino(sub.text)),
                ])

    return tetrominos

def loadTetrominos():
    path = Path.join(XMLDIR, "Tetrominos.xml")
    Log.log("Loading tetrominos from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadTetrominos(rf.read())
    except:
        raise ImportError("Error while loading tetrominos from `{}'".format(path))

def _loadOptions(json):
    return Json.loads(json)

def loadOptions():
    path = Path.join(JSONDIR, "Settings.json")
    return _loadOptions(_loadText(path))

def _loadSnapshot(data):
    return Pickle.loads(Bz2.decompress(data))

def loadSnapshot(seq):
    return _loadSnapshot(_loadText(Path.join(SNAPSHOTDIR, "{}.state.bz2".format(seq))))

def loadScoresMatching(**kwargs):
    scores = _loadScores(_loadText(Path.join(HIGHSCOREDIR, "Scores.xml")))
    for score in scores:
        if any(kwargs.get(thing) == score[thing] for thing in score):
            yield score

## XXX: Should this function work with the seq attribute? Or just the order of the scores in the file?
def loadScore(seq):
    scores = _loadScores(_loadText(Path.join(HIGHSCOREDIR, "Scores.xml")))
    return scores[seq]

