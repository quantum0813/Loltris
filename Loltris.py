#!/usr/bin/python2 -OO
#-*- coding: utf-8 -*--

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

import Log
import sys
import pygame
from Globals import *
Log.log("Firing up Loltris version {} from {!r}".format(VERSION, sys.argv[0]))

import Shared
import Menus
import Load
import Setup

if CENTER_WINDOW:
    os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.font.init()

## Run setup (will decide for itself whether or not it is necessary)
Setup.setupFiles()

## Load necessarry shared data
Shared.tetrominos = Load.loadTetrominos()
Shared.keymap = Load.loadKeymaps()
Shared.options = Load.loadOptions()

## Launch the game
Log.log("Creating MainMenu instance and running setup from Loltris startup script")
main_menu = Menus.MainMenu(caption="Loltris")
main_menu.setup()
Log.log("Running MainMenu from Loltris startup script")
main_menu.run()
