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
import os.path
import Log

DATADIR = "data"
FONTDIR = os.path.join(DATADIR, "Fonts")
XMLDIR = os.path.join(DATADIR, "XML")
IMAGEDIR = os.path.join(DATADIR, "Images")
MUSICDIR = os.path.join(DATADIR, "Music")
TXTDIR = os.path.join(DATADIR, "TXT")

## TODO: Switch to specifying the types manually everywhere
typeConvert = {
        None: lambda x: x,
        "int": lambda x: int(x.strip()),
        }

## As in duck-typing
def duck(text):
    if all(x.isdigit() or x.isspace() for x in text):
        return int(text.strip())
    return text.strip()

def loadHighscores(top=10):
    with open(os.path.join(XMLDIR, "Scores.xml")) as rf:
        return _loadScores(rf.read())[:top]

def _loadScores(xml):
    tree = ElementTree.XML(xml)
    scores = []
    for score in tree.getchildren():
        scores.append({})
        for info in score.getchildren():
            scores[-1][info.tag] = duck(info.text)
    return sorted(scores, key=lambda d: d["score"], reverse=True)

def _loadKeymaps(xml):
    tree = ElementTree.XML(xml)
    keymaps = {}
    for part in tree.getchildren():
        keymaps[part.tag] = {}
        for mapping in part.getchildren():
            keymaps[part.tag][mapping.tag] = int(mapping.text.strip("\n").strip(" "))
    return keymaps

def loadKeymaps():
    path = os.path.join(XMLDIR, "Keymap.xml")
    Log.log("Loading keymaps from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadKeymaps(rf.read())
    except:
        Log.panic("Error while loading keymaps from `{}'".format(path))
    return 

def _loadText(path):
    try:
        with open(path) as rf:
            return rf.read()
    except:
        Log.panic("Error while loading plain text from file `{}'".format(path))

def loadCredits():
    return _loadText(os.path.join(TXTDIR, "Credits.txt"))

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
    path = os.path.join(XMLDIR, "Tetrominos.xml")
    Log.log("Loading tetrominos from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadTetrominos(rf.read())
    except:
        raise ImportError("Error while loading tetrominos from `{}'".format(path))

def _loadOptions(json):
    pass

def loadOptions():
    pass
