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
import os.path
import Shared
import Log
import cPickle
import Dson
import bz2
import os
import pygame
from DataTypes import *
from Globals import *

INSTALL_DATA_LOCAL = "data"
DATADIR = os.path.join(os.path.expanduser("~"), ".loltris")
TTF_FONTDIR_LOCAL = os.path.join("Fonts", "TTF")
TTF_FONTDIR = os.path.join(DATADIR, TTF_FONTDIR_LOCAL)
BLOCKTEXT_FONTDIR_LOCAL = os.path.join("Fonts", "BlockText")
BLOCKTEXT_FONTDIR = os.path.join(DATADIR, BLOCKTEXT_FONTDIR_LOCAL)
IMAGEDIR_LOCAL = os.path.join("Images")
IMAGEDIR = os.path.join(DATADIR, IMAGEDIR_LOCAL)
TXTDIR_LOCAL = os.path.join("TXT")
TXTDIR = os.path.join(DATADIR, TXTDIR_LOCAL)
TETROMINODIR_LOCAL = os.path.join("Tetrominos")
TETROMINODIR = os.path.join(DATADIR, TETROMINODIR_LOCAL)
SETTINGSDIR_LOCAL = os.path.join("Settings")
SETTINGSDIR = os.path.join(DATADIR, SETTINGSDIR_LOCAL)
MUSICDIR_LOCAL = os.path.join("Music")
MUSICDIR = os.path.join(DATADIR, MUSICDIR_LOCAL)
## Not sure where this should be really
HIGHSCOREDIR_LOCAL = os.path.join("Highscores")
HIGHSCOREDIR = os.path.join(DATADIR, HIGHSCOREDIR_LOCAL)
SNAPSHOTDIR = os.path.join(HIGHSCOREDIR, "Snapshots")

LOCALDIRS = {
        TXTDIR_LOCAL,
        TTF_FONTDIR_LOCAL,
        BLOCKTEXT_FONTDIR_LOCAL,
        IMAGEDIR_LOCAL,
        TXTDIR_LOCAL,
        TETROMINODIR_LOCAL,
        SETTINGSDIR_LOCAL,
        MUSICDIR_LOCAL,
        }

def loadScores():
    path = os.path.join(HIGHSCOREDIR, "Scores.dson")
    Log.log("Loading scores from `{}'".format(path))
    return Dson.loads(_loadData(path))

def loadHighscores(top=10):
    path = os.path.join(HIGHSCOREDIR, "Scores.dson")
    Log.log("Loading highscores from `{}'".format(path))
    s = Dson.loads(_loadData(path))
    return sorted(s, key=lambda d: d["score"], reverse=True)[:top]

def loadKeymaps():
    path = os.path.join(SETTINGSDIR, "Keymaps.dson")
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
    Log.notice("Loading credits from {}".format(repr(os.path.join(TXTDIR, "Credits.txt"))))
    return _loadPlainText(os.path.join(TXTDIR, "Credits.txt"))

def loadTetrominos():
    tetrominos = []
    for filename in os.listdir(TETROMINODIR):
        path = os.path.join(TETROMINODIR, filename)
        Log.notice("Loading tetromino from {}".format(repr(path)))
        tetromino = cPickle.loads(bz2.decompress(_loadData(path)))
        tetrominos.append([
            tetromino["color"],
            filename.partition(".")[0],
            tetromino["matrix"],
            ])
    return tetrominos

def _loadOptions(dson):
    return Dson.loads(dson)

def loadOptions():
    path = os.path.join(SETTINGSDIR, "Settings.dson")
    Log.notice("Loading options from {}".format(repr(path)))
    return _loadOptions(_loadData(path))

def _loadSnapshot(data):
    return cPickle.loads(bz2.decompress(data))

def loadSnapshot(seq):
    Log.notice("Loading tetris snapshot from {}".format(repr(os.path.join(SNAPSHOTDIR, "{}.pyobj.bz2".format(seq)))))
    return _loadSnapshot(_loadData(os.path.join(SNAPSHOTDIR, "{}.pyobj.bz2".format(seq))))

def loadBlockFont(name):
    Log.notice("Loading BlockText font from {}".format(repr(os.path.join(BLOCKTEXT_FONTDIR, "{}.pyobj.bz2".format(name)))))
    return cPickle.loads(bz2.decompress(_loadData(os.path.join(BLOCKTEXT_FONTDIR, "{}.pyobj.bz2".format(name)))))

def loadImage(filename):
    if Shared.images.get(filename):
        return Shared.images[filename]
    Log.notice("Loading image {!r}".format(filename))
    Shared.images[filename] = pygame.image.load(os.path.join(IMAGEDIR, filename))
    return Shared.images[filename]

