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
from PythonShouldHaveTheseThingsByDefaultTheyAreJustTooFuckingHelpful import *

def makeUberTetromino(board):
    """ Creates a perfect tetromino (for the current board) """

    tetromino = []
    for y in xrange(board.height+1):
        if any(board.blocks.get((x, y)) for x in xrange(board.width+1)):
            break
    def clearUpwards(xpos, ypos):
        for y in xrange(ypos):
            if board.blocks.get((xpos, y)):
                return False
        return True
    for y in xrange(y, board.height+1):
        tetromino.append([clearUpwards(x, y) for x in xrange(0, board.width)])
    return Jobs.Tetromino(board, tetromino, "UBER", UBERCOLOR, xcenter=True)

def randomTetromino(board, updateinterval=FRAMERATE/2):
    """ Creates a random tetromino for a board, created for increased readability """
    color, type, matrix = Random.choice(Shared.tetrominos)
    return Jobs.Tetromino(board, matrix, type, color, xcenter=True, updateinterval=updateinterval)

class TetrisGame(Core.Game):
    def __init__(self, player_name="", *args, **kwargs):
        self.id = "TetrisGame"
        super(TetrisGame, self).__init__(self.id, *args, fill=True, soundtrack=os.path.join(Load.MUSICDIR, "uprising.ogg"), sound_enabled=SOUND_ENABLED, **kwargs)
        self.running = self.mainLoop
        self.highscores = Load.loadHighscores(top=HIGHSCORES)
        self.player_name = player_name

        ## All the jobs
        self.addJob("board",
                    Jobs.Board(self.screen,
                          x=SPACER,
                          y=SPACER,
                          height=BOARD_HEIGHT,
                          width=BOARD_WIDTH,
                          blockwidth=BOARD_BLOCKWIDTH,
                          level=kwargs.get("level", 1),
                          bgcolor=self.bgcolor
                          )
                    )
        self.addJob("tetromino", randomTetromino(self.jobs.board, updateinterval=FRAMERATE - (self.getJob("board").level-1)*UPDATEINTERVAL_DECREASE))
        color, _type, matrix = Random.choice(Shared.tetrominos)
        self.nextTetromino = Struct(color=color, type=_type, matrix=matrix)
        self.addJob("preview_window",
                    Jobs.Board(
                        self.screen,
                        x=SPACER+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                        y=SPACER,
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
                        x=SPACER+(BOARD_WIDTH)*BOARD_BLOCKWIDTH + SPACER,
                        yfit=True,
                        width=self.jobs.preview_window.width * BOARD_BLOCKWIDTH,
                        colors={"border":(0xaa,0xaa,0xaa), "font":(0xaa,0xaa,0xaa)},
                        font=TETRIS_STATUSBOX_FONT,
                        variables={
                            "level": lambda self: self.getJob("board").level,
                            "score": lambda self: self.getJob("board").score,
                            "lines": lambda self: self.getJob("board").lines,
                            "level up": lambda self: self.getJob("board").level_lines,
                            }
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

    def mainLoop(self):
        if not self.getJob("board").update_required and not hasattr(self.jobs, "window-game_over"):
            ## XXX: GAME OVER
            board = self.getJob("board")

            Log.log("Game over, displaying game state")
            matrix = [
                    [(x, y) in board.blocks for x in xrange(board.width)]
                    for y in xrange(board.height)
                    ]
            Matrix.put(matrix, f="_")

            if len(self.highscores) < HIGHSCORES or any(board.score > score["score"] for score in self.highscores):
                self.addJob("window-game_over", Jobs.Notification(self, "window-game_over", "New Highscore!"))
                Save.saveScores([{"name": self.player_name,
                                  "score": board.score,
                                  "level": board.level,
                                  "lines": board.lines,
                                  "state": self.jobs.board.blocks
                                  }])
            else:
                self.addJob("window-game_over", Jobs.Notification(self, "window-game_over", "Game Over"))
            self.addJob("endtimer", Jobs.TimedExecution(self.quitGame, seconds=2, anykey=True))

        if not self.jobs.tetromino.update_required and self.getJob("board").update_required:
            ## Create a new tetromino job from the nextTetromino Struct instance
            self.addJob("tetromino",
                        Jobs.Tetromino(
                            self.jobs.board,
                            self.nextTetromino.matrix, self.nextTetromino.type, self.nextTetromino.color,
                            xcenter=True, updateinterval=FRAMERATE - (self.getJob("board").level-1)*UPDATEINTERVAL_DECREASE))

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

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if event.key == Shared.keymap["game"]["pause"]:
                self.call(Menus.PauseMenu, caption="Tetris - Paused")

            if event.key == Shared.keymap["game"]["uber_tetromino"] and Shared.options.get("uber_tetromino"):
                self.addJob("tetromino", makeUberTetromino(self.getJob("board")))
