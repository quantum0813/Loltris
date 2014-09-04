#!/usr/bin/python

import Log, Load

tetrominos = []
keymap = {}
scores = []
options = {}
fonts = {}
images = {}
_loaded = False

def load():
    """ Load necessarry shared data """
    global tetrominos, keymap, options, _loaded

    if not _loaded:
        Log.log("Loading shared data")
        tetrominos = Load.loadTetrominos()
        keymap = Load.loadKeymaps()
        options = Load.loadOptions()
        _loaded = True
