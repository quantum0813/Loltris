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

if __name__ == '__main__':
    ## Run setup
    Setup.setupFiles()

    ## Load necessarry shared data
    Shared.tetrominos = Load.loadTetrominos()
    Shared.keymap = Load.loadKeymaps()
    Shared.options = Load.loadOptions()

    ## Launch the game
    Menus.MainMenu(caption="Loltris").run()
