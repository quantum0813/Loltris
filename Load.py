#!/usr/bin/python
#-*- coding: utf-8 -*-

from xml.etree import ElementTree
from RGB import rgbHexDecode
import os.path

DATADIR = "data"
XMLDIR = os.path.join(DATADIR, "XML")
IMAGEDIR = os.path.join(DATADIR, "Images")
MUSICDIR = os.path.join(DATADIR, "Music")

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
    print("Loading keymaps from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadKeymaps(rf.read())
    except:
        print("Error while loading keymaps from `{}'".format(path))
        raise ImportError

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
            print("Loading tetromino `{}' with color `{}'".format(sub_items["name"], sub_items["color"]))
        tetrominos.append([
                rgbHexDecode(sub_items["color"]),
                sub_items["name"],
                list(makeTetromino(sub.text)),
                ])

    return tetrominos

def loadTetrominos():
    path = os.path.join(XMLDIR, "Tetrominos.xml")
    print("Loading tetrominos from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadTetrominos(rf.read())
    except:
        print("Error while loading tetrominos from `{}'".format(path))
        raise ImportError
