#!/usr/bin/python
#-*- coding: utf-8 -*-

## =====================================================================
## Functions related to loading data from disk
## Copyright (C) 2014 Jonas Møller <jonasmo441@gmail.com>
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
import Shared
import Log
import cPickle as CPickle
import Dson
import bz2 as Bz2
import os as OS
import pygame as Pygame
from PSHTTBDTAJTFH import *
from Globals import *

DATADIR = "data"
TTF_FONTDIR = Path.join(DATADIR, "Fonts", "TTF")
BLOCKTEXT_FONTDIR = Path.join(DATADIR, "Fonts", "BlockText")
IMAGEDIR = Path.join(DATADIR, "Images")
MUSICDIR = Path.join(DATADIR, "Music")
TXTDIR = Path.join(DATADIR, "TXT")
JSONDIR = Path.join(DATADIR, "JSON")
TETROMINODIR = Path.join(DATADIR, "Tetrominos")
SETTINGSDIR = Path.join(DATADIR, "Settings")
## Not sure where this should be really
HIGHSCOREDIR = Path.join(DATADIR, "Highscores")
SNAPSHOTDIR = Path.join(HIGHSCOREDIR, "Snapshots")

def loadScores():
    path = Path.join(HIGHSCOREDIR, "Scores.dson")
    Log.log("Loading scores from `{}'".format(path))
    return Dson.loads(_loadData(path))

def loadHighscores(top=10):
    path = Path.join(HIGHSCOREDIR, "Scores.dson")
    Log.log("Loading highscores from `{}'".format(path))
    s = Dson.loads(_loadData(path))
    return sorted(s, key=lambda d: d["score"], reverse=True)[:top]

def loadKeymaps():
    path = Path.join(SETTINGSDIR, "Keymaps.dson")
    Log.log("Loading keymaps from `{}'".format(path))
    return Dson.loads(_loadData(path))

def _loadData(path):
    try:
        with open(path, "rb") as rf:
            return rf.read()
    except:
        Log.panic("Error while loading plain text from file `{}'".format(path))

def _loadPlainText(path):
    try:
        with open(path, "r") as fd:
            return fd.read().decode("utf-8")
    except:
        Log.panic("Error while loading plain text from file `{}'".format(path))

def loadCredits():
    Log.notice("Loading credits from {}".format(repr(Path.join(TXTDIR, "Credits.txt"))))
    return _loadPlainText(Path.join(TXTDIR, "Credits.txt"))

def loadTetrominos():
    tetrominos = []
    for filename in OS.listdir(TETROMINODIR):
        path = Path.join(TETROMINODIR, filename)
        Log.notice("Loading tetromino from {}".format(repr(path)))
        tetromino = CPickle.loads(Bz2.decompress(_loadData(path)))
        tetrominos.append([
            tetromino["color"],
            filename.partition(".")[0],
            tetromino["matrix"],
            ])
    return tetrominos

def _loadOptions(dson):
    return Dson.loads(dson)

def loadOptions():
    path = Path.join(SETTINGSDIR, "Settings.dson")
    Log.notice("Loading options from {}".format(repr(path)))
    return _loadOptions(_loadData(path))

def _loadSnapshot(data):
    return CPickle.loads(Bz2.decompress(data))

def loadSnapshot(seq):
    Log.notice("Loading tetris snapshot from {}".format(repr(Path.join(SNAPSHOTDIR, "{}.pyobj.bz2".format(seq)))))
    return _loadSnapshot(_loadData(Path.join(SNAPSHOTDIR, "{}.pyobj.bz2".format(seq))))

def loadBlockFont(name):
    Log.notice("Loading BlockText font from {}".format(repr(Path.join(BLOCKTEXT_FONTDIR, "{}.pyobj.bz2".format(name)))))
    return CPickle.loads(Bz2.decompress(_loadData(Path.join(BLOCKTEXT_FONTDIR, "{}.pyobj.bz2".format(name)))))

def loadImage(filename):
    if Shared.images.get(filename):
        return Shared.images[filename]
    Log.notice("Loading image {!r}".format(filename))
    Shared.images[filename] = Pygame.image.load(OS.path.join(IMAGEDIR, filename))
    return Shared.images[filename]

