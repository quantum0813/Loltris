#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Highscore explorer
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

import Core
import Load
import Shared
import Jobs
import pygame as Pygame
import Log
import JobQueue
from pygame.locals import *
from Globals import *

class Preview(Core.Game):
    def __init__(self, blocks, time=None, date=None, level=None, lines=None, name=None, score=None, seq=None, board_dimensions=None, *args, **kwargs):
        super(Preview, self).__init__("Preview", *args, fill=True, **kwargs)
        self.running = self.mainLoop

        self.addJob("board",
                    Jobs.Board(
                        self,
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
                        self, u"Date: {}\nTime: {}\nName: {}\nLines: {}\nLevel: {}\nScore: {}\n".format(date, time, name, lines, level, score),
                        border=True,
                        y=SPACER,
                        x=SPACER+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                        yfit=True,
                        width=BOARD_BLOCKWIDTH * PREVIEW_WIDTH,
                        colors=HIGHSCORE_EXPLORER_STATUSBOX_COLORSCHEME,
                        font=HIGHSCORE_EXPLORER_STATUSBOX_FONT,
                        fill=TETRIS_BACKGROUND,
                        )
                    )
        self.addJob(
                "exit_button",
                Jobs.TextBox(
                    self, "Exit", x=SPACER+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                    y=self.jobs.status.y + self.jobs.status.height + SPACER,
                    textfit=True, underline=True, colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)},
                    font=TETRIS_STATUSBOX_FONT, onmouseclick=self.quitGame, queue=JobQueue.SCROLL_FILLER + 1,
                    fill=TETRIS_BACKGROUND,
                    )
                )
        self.jobs.board.blocks = {}
        self.jobs.board.blocks.update(blocks)

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

    def mainLoop(self):
        pass

class HighscoreList(Core.Menu):
    def __init__(self, top=HIGHSCORES, header_font=MENU_HEADER_FONT, *args, **kwargs):
        super(HighscoreList, self).__init__("HighscoreList", *args, **kwargs)
        self.running = self.mainLoop
        self.scores = Load.loadScores()
        sorted_score_table = [(("Name", "Score", "Lines"), None)]
        sorted_score_table.extend([
                ((score["name"], score["score"], score["lines"]), score)
                for score in sorted(self.scores, key=lambda d: d["score"], reverse=True)
                ])
        self.header_font = {}
        self.header_font.update(header_font)
        self.addJob("header",
                Jobs.TextBox(
                    self, "Scores", y=20, xcenter=True, textfit=True, underline=False,
                    colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)}, font=self.header_font,
                    onmouseclick=self.onHeaderClick, queue=JobQueue.HEADER,
                    fill=TETRIS_BACKGROUND,
                    )
                )
        self.addJob(
                "table",
                Jobs.Table(
                    self, SPACER, self.jobs.header.y+self.jobs.header.height + 1, TETRIS_STATUSBOX_FONT, sorted_score_table,
                    colors=TETRIS_STATUSBOX_COLORSCHEME, onmouseclick=self.previewScore,
                    xcenter=True,# queue=JobQueue.TEXTBOX,
                    )
                )

        self.addJob(
                "exit_button",
                Jobs.TextBox(
                    self, "Exit", x=SPACER,
                    y=self.height - SPACER,
                    textfit=True, underline=True, colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)},
                    font=TETRIS_STATUSBOX_FONT, onmouseclick=self.quitGame, queue=JobQueue.SCROLL_FILLER + 1,
                    fill=TETRIS_BACKGROUND,
                    )
                )
        self.jobs.exit_button.y -= self.jobs.exit_button.height

        ## Keeps the exit_button from being overwritten by the table
        self.addJob(
                "bottom_filler",
                Jobs.Filler(
                    self,
                    0, self.jobs.exit_button.y - SPACER,
                    self.width, self.jobs.exit_button.height + (self.height - self.jobs.exit_button.y) + SPACER,
                    queue=JobQueue.SCROLL_FILLER,
                    )
                )
        ## Keeps the table from being visible above the header
        self.addJob(
                "top_filler",
                Jobs.Filler(
                    self, 0, 0, self.width, self.jobs.header.y,
                    queue=JobQueue.SCROLL_FILLER,
                    )
                )

    def previewScore(self, seq, row, reference):
        ## Don't do anything if the user clicks on the header.
        if not seq:
            return
        blocks = Load.loadSnapshot(reference["seq"])
        self.call(Preview, blocks, **reference)

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5 and (self.jobs.table.y + self.jobs.table.height - self.height + self.jobs.bottom_filler.height) >= 0:
                ## DOWN
                self.jobs.table.y -= 4
            if event.button == 4 and self.jobs.table.y < self.jobs.header.y + self.jobs.header.height:
                ## UP
                self.jobs.table.y += 4

    def mainLoop(self):
        pass

