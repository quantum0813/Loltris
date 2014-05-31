#!/usr/bin/python
#-*- coding: utf-8 -*-

## =====================================================================
## Tetromino creator (helper)
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


import Jobs
import Core
import Shared
import Log
import Matrix
import Save
import Load
import pygame as Pygame
from Globals import *
from pygame.locals import *

def islands(dictionary):
    class Block(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.neighbours = []

    def neighbours(x, y):
        positions = [(x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1),
                     (x, y-1), (x-1, y), (x, y+1), (x+1, y), ]
        return (pos for pos in positions if pos in dictionary)

    def traverse(block, visited):
        if (block.x, block.y) in visited:
            return
        visited.add((block.x, block.y))
        for block in block.neighbours:
            traverse(block, visited)

    blocks = {}
    for x, y in dictionary:
        blocks[(x, y)] = Block(x, y)
    for block in blocks:
        blocks[block].neighbours = set([blocks[pos] for pos in neighbours(blocks[block].x, blocks[block].y)])

    visited = set()
    traverse(blocks[block], visited)

    return set(blocks).difference(visited)

class MakeTetromino(Core.Game):
    def __init__(self, *args, **kwargs):
        self.id = "MakeTetromino"
        super(MakeTetromino, self).__init__(
                self.id, *args, fill=False, **kwargs)
        self.running = self.mainLoop

        ## TODO: The user should be able to change the color, create a "color palette thingy"
        self.color = (0xbb,0xbb,0xbb)

        self.addJob(
                "board",
                Jobs.Board(
                    self,
                    x=SPACER,
                    y=SPACER,
                    height=BOARD_HEIGHT,
                    width=BOARD_WIDTH,
                    blockwidth=BOARD_BLOCKWIDTH,
                    level=0,
                    bgcolor=self.bgcolor,
                    )
                )

        ## TODO: Make it less cumbersome and repeditive to spawn a row of buttons
        self.addJob(
                "save_button",
                Jobs.TextBox(self, "Save", x=self.jobs.board.x + (self.jobs.board.blocks_width*self.jobs.board.blockwidth) + 5,
                        y=self.jobs.board.y, 
                        textfit=True, underline=True, colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)},
                        font=TETRIS_STATUSBOX_FONT, onmouseclick=self.save,
                        )
                )
        self.addJob(
                "clear_button",
                Jobs.TextBox(self, "Clear", x=self.jobs.board.x + (self.jobs.board.blocks_width*self.jobs.board.blockwidth) + 5,
                        y=self.jobs.board.y + self.jobs.save_button.height + MAKETETROMINO_OPTION_SPACER,
                        textfit=True, underline=True, colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)},
                        font=TETRIS_STATUSBOX_FONT, onmouseclick=self.clear,
                    )
                )
        self.addJob(
                "exit_button",
                Jobs.TextBox(self, "Exit", x=self.jobs.board.x + (self.jobs.board.blocks_width*self.jobs.board.blockwidth) + 5,
                        y=self.jobs.clear_button.y + self.jobs.clear_button.height + MAKETETROMINO_OPTION_SPACER,
                        textfit=True, underline=True, colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)},
                        font=TETRIS_STATUSBOX_FONT, onmouseclick=self.quitGame,
                    )
                )
        self.addJob(
                "color_button",
                Jobs.TextBox(self, "Change color", x=self.jobs.board.x + (self.jobs.board.blocks_width*self.jobs.board.blockwidth) + 5,
                        y=self.jobs.exit_button.y + self.jobs.exit_button.height + MAKETETROMINO_OPTION_SPACER,
                        textfit=True, underline=True, colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)},
                        font=TETRIS_STATUSBOX_FONT, onmouseclick=self.changeColor,
                    )
                )

    def clear(self):
        self.jobs.board.blocks = {}

    def changeColor(self):
        pass

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button in (1, 3):
                x, y = self.jobs.board.getBlockInPos(*Pygame.mouse.get_pos())
                if x > self.jobs.board.blocks_width-1 or y > self.jobs.board.height-1 or x < 0 or y < 0:
                    pass
                elif not self.jobs.board.blocks.get((x, y)):
                    self.jobs.board.blocks[(x, y)] = self.color
                    self.jobs.board.drawCube(x, y, self.color)
                else:
                    self.jobs.board.blocks.pop((x, y))
                    self.jobs.board.emptyBlocks()

    def save(self):
        if not self.jobs.board.blocks:
            Log.log("No blocks present, will not save tetromino")
            self.addJob("no_blocks_present", Jobs.Notification(self, "no_blocks_present", "Invalid: No blocks present"))
            return

        if any(islands(self.jobs.board.blocks)):
            Log.log("Islands present, will not save tetromino")
            self.addJob( "islands_present_window", Jobs.Notification(self, "islands_present_window", "Invalid: Islands present"))
            return

        xlow = min(x for x, y in self.jobs.board.blocks)
        xhigh = max(x for x, y in self.jobs.board.blocks)
        ylow = min(y for x, y in self.jobs.board.blocks)
        yhigh = max(y for x, y in self.jobs.board.blocks)
        matrix = [
                [(x, y) in self.jobs.board.blocks for x in xrange(xlow, xhigh+1)]
                for y in xrange(ylow, yhigh+1)
                ]

        Log.log("Created new tetromino, displaying below")
        Matrix.put(matrix)
        Save.saveTetromino(self.color, "kek", matrix)
        Shared.tetrominos = Load.loadTetrominos()

        return True

    def mainLoop(self):
        pass

class Browse(Core.Game):
    def __init__(self, *args, **kwargs):
        super(Browse, self).__init__(
                "Browse", *args, fill=True, **kwargs)
