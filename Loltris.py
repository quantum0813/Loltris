#!/usr/bin/python2
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
import profile as Profile
import pygame as Pygame

if __name__ == '__main__':
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
    # Profile.run("main_menu.run()")
    main_menu.run()
