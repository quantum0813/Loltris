#!/usr/bin/python
#-*- coding: utf-8 -*-

## =====================================================================
## Yup, it's tetris
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
import Matrix
import os.path
import Load
import Shared
import Jobs
import Menus
import Log
import Save
import random as Random
import pygame as Pygame
from Globals import *
from pygame.locals import *
from PSHTTBDTAJTFH import *

def makeUberTetromino(board):
    """ Creates a perfect tetromino (for the current board) """

    tetromino = []
    for y in xrange(board.blocks_height+1):
        if any(board.blocks.get((x, y)) for x in xrange(board.blocks_width+1)):
            break
    def clearUpwards(xpos, ypos):
        for y in xrange(ypos):
            if board.blocks.get((xpos, y)):
                return False
        return True
    for y in xrange(y, board.blocks_height+1):
        tetromino.append([clearUpwards(x, y) for x in xrange(0, board.blocks_width)])
    return Jobs.Tetromino(board, tetromino, "UBER", UBERCOLOR, xcenter=True)

def randomTetromino(board, updateinterval=TETRIS_FRAMERATE/2):
    """ Creates a random tetromino for a board, created for increased readability """
    color, type, matrix = Random.choice(Shared.tetrominos)
    return Jobs.Tetromino(board, matrix, type, color, xcenter=True, updateinterval=updateinterval)

class TetrisInterface(Jobs.Job):
    def __init__(self, game, x, y, keymap=None, **kwargs):
        super(TetrisInterface, self).__init__(
                game, x, y, **kwargs
                )

        self.keymap = keymap or Shared.keymap["game"]["player1"]

        ## All the jobs
        self.addJob("board",
                    Jobs.Board(
                        self,
                        x=self.x,
                        y=self.y,
                        height=BOARD_HEIGHT,
                        width=BOARD_WIDTH,
                        blockwidth=BOARD_BLOCKWIDTH,
                        level=kwargs.get("level", 1),
                        bgcolor=self.bgcolor,
                        )
                    )

        color, type, matrix = Random.choice(Shared.tetrominos)
        self.addJob("tetromino",
                Jobs.Tetromino(
                    self.jobs.board, matrix, type, color, xcenter=True, updateinterval=TETRIS_FRAMERATE - (self.getJob("board").level-1)*UPDATEINTERVAL_DECREASE,
                    keymap=keymap or Shared.keymap["game"]["player1"]
                    )
                )

        color, _type, matrix = Random.choice(Shared.tetrominos)
        self.nextTetromino = Struct(color=color, type=_type, matrix=matrix)
        self.addJob("preview_window",
                    Jobs.Board(
                        self,
                        x=self.x+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                        y=self.y,
                        height=PREVIEW_HEIGHT,
                        width=PREVIEW_WIDTH,
                        blockwidth=BOARD_BLOCKWIDTH,
                        bgcolor=self.bgcolor,
                        draw_grid=False,
                        )
                    )
        self.addJob("status",
                    Jobs.TextBox(
                        self, "Level: {level}\nScore: {score}\nLines: {lines}\nLines left: {level up}",
                        border=True,
                        y=self.jobs.preview_window.y + (PREVIEW_HEIGHT * BOARD_BLOCKWIDTH) + SPACER,
                        x=self.x+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                        yfit=True,
                        width=self.jobs.preview_window.width,
                        colors=TETRIS_STATUSBOX_COLORSCHEME,
                        font=TETRIS_STATUSBOX_FONT,
                        variables={
                            "level": lambda self: self.getJob("board").level,
                            "score": lambda self: self.getJob("board").score,
                            "lines": lambda self: self.getJob("board").lines,
                            "level up": lambda self: self.getJob("board").level_lines,
                            },
                        fill=TETRIS_BACKGROUND,
                        )
                    )
        self.addJob("preview_block",
                    Jobs.Tetromino(
                        self.jobs.preview_window,
                        self.nextTetromino.matrix,
                        self.nextTetromino.type,
                        self.nextTetromino.color,
                        xcenter=True,
                        ycenter=True,
                        ghostpiece=False))
        self.jobs.preview_block.update_required = False
        self.width = SCREEN_WIDTH // 2
        self.height = SCREEN_HEIGHT

    def update(self):
        super(TetrisInterface, self).update()

        if not self.jobs.tetromino.update_required and self.jobs.board.update_required:
            ## Create a new tetromino job from the nextTetromino Struct instance
            self.addJob("tetromino",
                        Jobs.Tetromino(
                            self.jobs.board,
                            self.nextTetromino.matrix, self.nextTetromino.type, self.nextTetromino.color,
                            xcenter=True, updateinterval=TETRIS_FRAMERATE - (self.jobs.board.level-1)*UPDATEINTERVAL_DECREASE,
                            keymap=self.keymap
                            ))

            ## Get the next tetromino information, create a Struct instance that stores this information,
            ## then create another preview block.
            color, _type, matrix = Random.choice(Shared.tetrominos)
            self.nextTetromino = Struct(color=color, type=_type, matrix=matrix)
            self.addJob("preview_block",
                        Jobs.Tetromino(
                            self.jobs.preview_window,
                            self.nextTetromino.matrix, self.nextTetromino.type, self.nextTetromino.color,
                            xcenter=True, ycenter=True, ghostpiece=False))
            self.jobs.preview_block.update_required = False

class TetrisGame(Core.Game):
    def __init__(self, *args, **kwargs):
        self.id = "TetrisGame"
        super(TetrisGame, self).__init__(
                self.id, *args, fill=True, soundtrack=os.path.join(Load.MUSICDIR, "uprising.ogg"), sound_enabled=SOUND_ENABLED, **kwargs
                )
        self.running = self.mainGame
        self.highscores = Load.loadHighscores(top=HIGHSCORES)

        self.addJob("interface", TetrisInterface(self, SPACER, SPACER))

    def getName(self):
        if not self.jobs.name_inputbox.update_required:
            Save.saveScore({"name": self.jobs.name_inputbox.value,
                            "score": self.jobs.interface.jobs.board.score,
                            "level": self.jobs.interface.jobs.board.level,
                            "lines": self.jobs.interface.jobs.board.lines,
                            },
                            state=self.jobs.interface.jobs.board.blocks,
                            )
            self.quitGame()

    def mainGame(self):
        if not self.jobs.interface.jobs.board.update_required and not hasattr(self.jobs, "window-game_over"):
            ## XXX: GAME OVER
            board = self.jobs.interface.jobs.board

            Log.log("Game over, displaying game state")
            matrix = [
                    [(x, y) in board.blocks for x in xrange(board.blocks_width)]
                    for y in xrange(board.blocks_height)
                    ]
            Matrix.put(matrix, f="_")

            if ((len(self.highscores) < HIGHSCORES or any(board.score > score["score"] for score in self.highscores)) and 
                    not Shared.options.get("uber_tetromino") and not Shared.options.get("flip_tetromino")
                    ):
                self.addJob("name_inputbox", Jobs.InputBox(self, "New Highscore!\nName: "))
                self.running = self.getName
            else:
                self.addJob("window-game_over", Jobs.Notification(self, "window-game_over", "Game Over"))
                self.addJob("endtimer", Jobs.TimedExecution(self.quitGame, seconds=3, anykey=True))

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if event.key == Shared.keymap["game"]["pause"]:
                self.call(Menus.PauseMenu, sound_enabled=False, caption="Tetris - Paused")

            if event.key == Shared.keymap["game"]["player1"]["uber_tetromino"] and Shared.options["gameplay"].get("uber_tetromino"):
                self.addJob("tetromino", makeUberTetromino(self.jobs.interface.jobs.board))

