#!/usr/bin/python2 -OO
#-*- coding: utf-8 -*-

## =====================================================================
## Launcher for Loltris
## 
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

doc = """
Usage:
    loltris [--loglevel=n] [--dev]
    loltris (-h | --help | --version | -v)

Options:
    loltris --help,-h        Loltris documentation
    loltris --version,-v     Print the loltris version and exit
    loltris --loglevel=n     Set loglevel, 0="ONLY CRITICAL" 5="ALL"
"""

import sys
import docopt

from Globals import *

nice_version = "Loltris v{}".format(VERSION)
args = docopt.docopt(doc, version=nice_version)

## Launch the game
if args["-h"] or args["--help"]:
    print(doc)
    sys.exit()
if args["-v"]:
    print(nice_version)
    sys.exit()

import Menus
import Init
Init.initGame(Menus.MainMenu, caption="Loltris").run()
