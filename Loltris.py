#!/usr/bin/python2 -OO
#-*- coding: utf-8 -*--

## =====================================================================
## Launcher for a Tetris clone written in Python/Pygame, with some
## weird features.
## 
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

import Shared
import Menus
import Load
import Setup
import Log
import profile as Profile
import os as OS
import pygame as Pygame
from Globals import *

if __name__ == '__main__':
    if CENTER_WINDOW:
        OS.environ["SDL_VIDEO_CENTERED"] = "1"

    Pygame.font.init()

    ## Run setup (will decide for itself whether or not it is necessary)
    Setup.setupFiles()

    ## Load necessarry shared data
    Shared.tetrominos = Load.loadTetrominos()
    Shared.keymap = Load.loadKeymaps()
    Shared.options = Load.loadOptions()

    ## Launch the game
    main_menu = Menus.MainMenu(caption="Loltris")
    main_menu.setup()
    Log.log("Running MainMenu from Loltris startup script")
    main_menu.run()
else:
    Log.warning("Importing from Loltris launcher")

