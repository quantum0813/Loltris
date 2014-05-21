#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Highscore explorer
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

import Core
import Shared
import pygame as Pygame
from pygame.locals import *
from Globals import *

class HighscoreList(Core.Game):
    def __init__(self, top=HIGHSCORES, *args, **kwargs):
        super(HighscoreList, self).__init__("HighscoreList", *args, **kwargs)
        self.running = self.mainLoop

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

    def mainLoop(self):
        pass

