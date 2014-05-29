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
import Load
import Shared
import Jobs
import pygame as Pygame
import Log
from pygame.locals import *
from Globals import *

class Preview(Core.Game):
    def __init__(self, blocks, date=None, level=None, lines=None, name=None, score=None, *args, **kwargs):
        super(Preview, self).__init__("Preview", *args, fill=True, **kwargs)
        self.running = self.mainLoop

        self.addJob("board",
                    Jobs.Board(self.screen,
                          x=SPACER,
                          y=SPACER,
                          height=BOARD_HEIGHT,
                          width=BOARD_WIDTH,
                          blockwidth=BOARD_BLOCKWIDTH,
                          level=kwargs.get("level", 1),
                          bgcolor=self.bgcolor,
                          )
                )
        kwargs.pop("screen")
        self.addJob("status",
                    Jobs.TextBox(
                        self, "Date: {}\nName: {}\nLines: {}\nLevel: {}\nScore: {}\n".format(date, name, lines, level, score),
                        border=True,
                        y=SPACER,
                        x=SPACER+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                        yfit=True,
                        width=BOARD_BLOCKWIDTH * PREVIEW_WIDTH,
                        colors=TETRIS_STATUSBOX_COLORSCHEME,
                        font=TETRIS_STATUSBOX_FONT,
                        )
                    )
        ## XXX: Beware that this dict is RW
        self.jobs.board.blocks = blocks

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

    def mainLoop(self):
        pass

class HighscoreList(Core.Menu):
    def __init__(self, top=HIGHSCORES, *args, **kwargs):
        super(HighscoreList, self).__init__("HighscoreList", *args, **kwargs)
        self.running = self.mainLoop
        self.scores = Load.loadScores()
        table_list = [(score["name"], score["score"]) for score in self.scores]
        self.addJob(
                "table",
                Jobs.Table(
                    self, SPACER, SPACER, TETRIS_STATUSBOX_FONT, table_list,
                    colors=TETRIS_STATUSBOX_COLORSCHEME,
                    )
                )

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

    def mainLoop(self):
        pass

