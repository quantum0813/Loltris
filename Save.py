#!/usr/bin/python
#-*- coding: utf-8 -*--

from Load import IMAGEDIR, XMLDIR, MUSICDIR, DATADIR
# from lxml.etree import ElementTree
import lxml.etree as ElementTree
import os.path

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

