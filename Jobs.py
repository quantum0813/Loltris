#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## All the jobs (or game objects) used in Game derived instances
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

import pygame as Pygame
import Queue
import Load
import Log
import Utils
import Shared
import Matrix
import os.path
from pygame.locals import *
from Globals import *

## The basic structure of a Job
class Job(object):
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    def forceDraw(self):
        pass

    def draw(self):
        pass

    def eventHandler(self, event):
        pass

    def update(self):
        pass

class TextBox(object):
    def __init__(self, game, text, colors={"background": (0,0,0)}, border=False, ycenter=False, underline=False, background=False,
                 xcenter=False, x=0, y=0, height=0, width=0, textfit=False, yfit=False, xfit=False, font={"name": ""}, padding=12,
                 queue=None, variables={}, updatewhen=None, onmouseclick=None, onmouseenter=None, onmouseleave=None, fill=True):

        # Log.log("Initializing TextBox for `{}' with {}".format(
        #     game.id, repr(text) if len(repr(text)) < 20 else repr(text)[:17]+"...'"))

        if not text:
            raise TypeError("No text given to TextBox")

        self.game = game
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border = border
        self.colors = colors
        self.borderwidth = 1
        self.update_required = True
        self.draw_required = True
        self.xpadding = 0
        self.ypadding = 0
        self.underline = underline
        self.background = background
        self.queue = queue if queue != None else Queue.TEXTBOX
        self.text = text
        self.font = font
        self.textfit = textfit
        self.ycenter = ycenter
        self.xcenter = xcenter
        self.padding = padding
        self.variables = variables
        self.fill = fill
        self.xfit = xfit
        self.yfit = yfit

        ## Mouse-related business
        self.onmouseclick = onmouseclick
        self.onmouseenter = onmouseenter
        self.onmouseleave = onmouseleave
        self.hasmouse = False

        ## XXX: Hold that thought
        self.updatewhen = updatewhen

        self.renderFonts()

        ## Copy from colors
        self.colors = {}
        for color in colors:
            self.colors[color] = colors[color]

    def renderFonts(self):
        variables = {}

        for var in self.variables:
            variables[var] = self.variables[var](self.game)
        text = self.text.format(**variables)

        if not self.font.get("name"):
            self.font["name"] = Pygame.font.get_default_font()
        fontobj = Shared.globfonts.get(Utils.genKey(self.font))
        if not fontobj:
            try:
                fontobj = Shared.globfonts[Utils.genKey(self.font)] = \
                        Pygame.font.Font(
                                os.path.join(Load.FONTDIR, "{}.ttf".format(self.font["name"])),
                                self.font.get("size", 40),
                                bold=self.font.get("bold"),
                                italic=self.font.get("italic")
                                )
            except IOError:
                Log.panic("Unable to load font: `{}' for {}".format(self.font["name"], self))

        self.rendered_fonts = []
        self.fontwidth = 0
        self.fontheight = 0
        for line in text.splitlines():
            self.rendered_fonts.append(fontobj.render(line.rstrip("\n"), True, self.colors["font"]))
            width, height = fontobj.size(line)
            self.fontwidth = self.fontwidth if self.fontwidth > width else width
        self.fontheight = height

        if self.textfit:
            ## XXX: LEGACY
            self.yfit = True
            self.xfit = True

        if self.xfit:
            self.width = self.fontwidth
            self.xpadding = (self.width/self.padding)
            self.width += self.xpadding
        if self.yfit:
            self.height = self.fontheight*len(self.rendered_fonts)
            self.ypadding = (self.height/self.padding)
            self.height += self.ypadding

        if self.xcenter:
            self.x = (self.game.width / 2) - (self.width / 2)
        if self.ycenter:
            self.y = (self.game.height / 2) - (self.height / 2)

    def draw(self):
        ## XXX: Hold that thought
        # if self.updatewhen:
        #     for update in updatewhen:
        #         pass

        ## FIXME: SHOULD NOT BE DONE ON EVERY SINGLE DRAW
        ##        In order to avoid this I need to implement "updatewhen".
        self.renderFonts()

        if self.background:
            Pygame.draw.rect(
                    self.game.screen,
                    self.colors["background"],
                    (self.x, self.y, self.width, self.height),
                    0,
                    )
        if self.border:
            Pygame.draw.rect(
                    self.game.screen,
                    self.colors["border"],
                    (self.x-self.borderwidth, self.y-self.borderwidth, self.width+self.borderwidth, self.height+self.borderwidth),
                    self.borderwidth,
                    )

        spos = self.y + self.ypadding/2
        for f in self.rendered_fonts:
            self.game.screen.blit(f, (self.x + self.xpadding/2, spos))
            spos += self.fontheight
        if self.underline:
            Pygame.draw.line(
                    self.game.screen,
                    self.colors["font"],
                    (self.x, spos),
                    (self.x + self.width, spos),
                    )

    def eventHandler(self, event):

        if event.type == MOUSEMOTION:
            isin = Utils.isInCube(Pygame.mouse.get_pos(), (self.x, self.y, self.width, self.height))
            if isin and not self.hasmouse:
                self.hasmouse = True
                if self.onmouseenter:
                    self.onmouseenter(self)
            if not isin and self.hasmouse:
                self.hasmouse = False
                if self.onmouseleave:
                    self.onmouseleave(self)

        if event.type == MOUSEBUTTONDOWN and self.onmouseclick:
            if Utils.isInCube(Pygame.mouse.get_pos(), (self.x, self.y, self.width, self.height)):
                Log.debug("Mouseclick on `{}'".format(self))
                self.onmouseclick()
                self.game.lock[MOUSEBUTTONDOWN] = self

    def update(self):
        pass

class Slider(TextBox):
    def __init__(self, game, text, x=0, y=0, height=5, width=0, colors=None):
        self.colors = colors or {
                "background": (0,0,0),
                "filled": (0,0,0),
                "empty": (0,0,0),
                "slider": (0,0,0),
                }

        super(Slider, self).__init__(
                game, text, x=x, y=y, background=True, colors=colors,
                )
        self.onmouseclick = lambda: self.moveBar(Pygame.mouse.get_pos()[0])

    def getPercentage(self):
        pass

class Flipper(TextBox):
    def __init__(self, game, title, options, x=0, y=0, height=5, width=0, colors=None):
        super(Flipper, self).__init__(
                game, title + options[0], x=x, y=y, background=True, colors=colors,
                )
        self.option = 0
        self.title = title

    def nextOption(self):
        if self.option+1 == len(self.options):
            self.option = 0
        else:
            self.option += 1
        self.text = self.title + self.options[self.option]
        self.renderFonts()

    def previousOption(self):
        if self.option == 0:
            self.option == len(self.options)-1
        else:
            self.option -= 1
        self.text = self.title + self.options[self.option]
        self.renderFonts()

class Switch(TextBox):
    """ On/Off option, will display a box, which will either be empty or crossed depending on
        the state of the option.
    """
    def __init__(self, game, text, whenon, whenoff, ison=False, box_center=False, boxwidth=None, box_offset=0, **kwargs):
        Log.debug("Initializing Switch instance")
        super(Switch, self).__init__(game, text, textfit=True, onmouseclick=self.flip, **kwargs)
        self.whenoff = whenoff
        self.whenon = whenon
        self.on = ison
        self.box_offset = box_offset

        self.boxwidth = boxwidth
        if not boxwidth:
            self.boxwidth = self.height // 2
        if box_center:
            self.box_offset = (self.height // 2) - (self.boxwidth // 2)
            self.y_center = self.y + self.height // 2
        self.width += self.boxwidth

    def flip(self):
        self.on = not self.on
        if self.on:
            self.whenon()
        else:
            self.whenoff()

    def drawBox(self):
        Pygame.draw.rect(
                self.game.screen,
                self.colors.get("checkbox", (0,0,0)),
                (self.x + self.width, self.y + self.box_offset, self.boxwidth, self.boxwidth),
                1)

        if self.on:
            Pygame.draw.rect(
                self.game.screen,
                self.colors.get("on", (0,0,0)),
                (self.x + self.width + 1, self.y + self.box_offset + 1, self.boxwidth-1, self.boxwidth-1),
                )
        else:
            Pygame.draw.rect(
                self.game.screen,
                self.colors.get("off", (0,0,0)),
                (self.x + self.width + 1, self.y + self.box_offset + 1, self.boxwidth-2, self.boxwidth-2),
                )

    def draw(self):
        super(Switch, self).draw()
        self.drawBox()

class TimedExecution(object):
    def __init__(self, function, cycles=0, seconds=0, timed=True, anykey=True):
        self.update_required = True
        self.draw_required = False
        self.queue = 0
        self.anykey = True
        self.function = function
        self.timed = timed
        self.fill = False

        self.cycles = 0
        if cycles:
            self.cycles = cycles
        elif seconds:
            self.cycles = seconds * FRAMERATE

    def eventHandler(self, event):
        if event.type == KEYDOWN and self.anykey:
            self.update_required = False
            self.function()

    def draw(self):
        pass

    def update(self):
        if self.cycles <= 0 and self.timed:
            self.update_required = False
            self.function()
        self.cycles -= 1

class Tetromino(object):
    def __init__(self, board, matrix, _type, color, x=0, y=None, ycenter=False,
                 xcenter=False, ghostpiece=True, updateinterval=FRAMERATE, queue=None,
                 fill=False,
                 ):

        if not matrix:
            raise TypeError("Will not create tetromino with empty matrix")

        self.matrix = matrix
        self.type = _type
        self.board = board
        self.color = color
        self.updateinterval = updateinterval
        self.time_until_update = self.updateinterval
        self.draw_required = True
        self.update_required = True
        self.sped_up = False
        self.x = x
        self.y = y
        self.queue = queue if queue != None else Queue.TETROMINO
        self.level = 1
        self.fill = fill
        self.width = len(self.matrix[0]) * BOARD_BLOCKWIDTH
        self.height = len(self.matrix) * BOARD_BLOCKWIDTH

        if xcenter:
            self.x = (self.board.width//2) - (len(self.matrix[0])//2)

        if y == None:
            self.y = -(len(self.matrix))
        if ycenter:
            self.y = (self.board.height//2) - (len(self.matrix)//2)

        self.ghostpiece = None
        if ghostpiece:
            self.ghostpiece = GhostTetromino(board, matrix, _type, GHOST_COLOR, x=x, y=y, xcenter=xcenter)
            self.ghostpiece.drop(self.y)

    def getActiveBlocks(self):
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                if self.matrix[y][x]:
                    yield self.x + x, self.y + y

    def draw(self):
        if self.ghostpiece:
            self.ghostpiece.draw()
        for x, y in self.getActiveBlocks():
            self.board.drawCube(x, y, self.color)

    def insert(self):
        if self.y < 0:
            ## XXX: GAME OVER
            self.board.update_required = False

        for x, y in self.getActiveBlocks():
            self.board.blocks[(x, y)] = self.color
        self.board.checkTetris()
        self.update_required = False

    def update(self):
        self.time_until_update -= 1
        if self.time_until_update <= 0:
            self.moveDiagonal(1)
            self.time_until_update = self.updateinterval

    def drop(self):
        while self.update_required:
            self.moveDiagonal(1)

    def checkBlockCollision(self):
        return any(self.board.blocks.get((x, y)) for x, y in self.getActiveBlocks())

    def checkWallCollision(self, xp, yp):
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                ## Some of the functions need to know which edge the collision happened on,
                ## otherwise the result can be treated like a boolean.
                if self.matrix[y][x]:
                    if yp+y > self.board.height-1:
                        return "bottom"
                    if xp+x > self.board.width-1:
                        return "right"
                    if xp+x < 0:
                        return "left"

    ## Move diagonally, if possible
    def moveDiagonal(self, direction):
        self.y += direction
        if self.checkBlockCollision():
            self.y -= direction
            self.insert()
        if self.checkWallCollision(self.x, self.y) == "bottom":
            self.y -= direction
            self.insert()

    ## Move horizontally, if possible
    def moveHorizontal(self, direction):
        self.updateGhost("moveHorizontal", direction)
        self.x += direction
        if self.checkBlockCollision():
            self.x -= direction
        if self.checkWallCollision(self.x, self.y):
            self.x -= direction

    ## Rotate if possible
    def rotate(self, direction):
        last_matrix = self.matrix
        self.matrix = Matrix.rot90(self.matrix)
        if self.checkWallCollision(self.x, self.y) or self.checkBlockCollision():
            self.matrix = last_matrix
        else:
            self.updateGhost("rotate", direction)

    def updateGhost(self, attr, *args, **kwargs):
        if self.ghostpiece:
            self.ghostpiece.y = self.y
            self.ghostpiece.x = self.x
            getattr(self.ghostpiece, attr)(*args, **kwargs)
            self.ghostpiece.drop(self.y)

    ## It makes the game WAAY to easy, but i kind of always wondered "what if"
    def flip(self):
        if not (self.checkWallCollision(self.x, self.y) or self.checkBlockCollision()):
            Matrix.flip(self.matrix)
            self.updateGhost("flip")

    def eventHandler(self, event):
        if event.type == KEYUP:
            if event.key == Shared.keymap["game"]["speed_up"] and self.sped_up:
                self.sped_up = False
                self.updateinterval = self.normal_speed
                self.time_until_update = self.updateinterval

        if event.type == KEYDOWN:
            if event.key == Shared.keymap["game"]["rotate_right"]:
                self.rotate(1)
            elif event.key == Shared.keymap["game"]["rotate_left"]:
                self.rotate(-1)
            elif event.key == Shared.keymap["game"]["reverse"] and Shared.options.get("flip_tetromino"):
                self.flip()

            elif event.key == Shared.keymap["game"]["move_right"]:
                self.moveHorizontal(1)
            elif event.key == Shared.keymap["game"]["move_left"]:
                self.moveHorizontal(-1)

            elif event.key == Shared.keymap["game"]["drop_down"]:
                self.drop()

            elif event.key == Shared.keymap["game"]["speed_up"]:
                self.sped_up = True
                self.normal_speed = self.updateinterval
                self.updateinterval = SPED_UP_UPDATEINTERVAL
                self.time_until_update = self.updateinterval

## This object will be managed by a Tetromino(), it should not be managed as a Job
class GhostTetromino(Tetromino):
    def __init__(self, *args, **kwargs):
        super(GhostTetromino, self).__init__(*args, ghostpiece=False, **kwargs)

    def drop(self, y_pos):
        for y in xrange(y_pos, self.board.height):
            self.y = y
            if self.checkBlockCollision() or self.checkWallCollision(self.x, self.y) == "bottom":
                ## We need to be one step away from the next collision
                self.y -= 1
                break

class InputBox(TextBox):
    def __init__(self, prompt):
        super(InputBox, self).__init__(
                "{prompt}{input}",
                variables={
                    "input": lambda self: self.jobs.board.level,
                    "prompt": lambda self: self.prompt,
                    }
                )

class AutoTextBox(TextBox):
    def __init__(self, game, text, **kwargs):
        super(AutoTextBox, self).__init__(
                game, text, textfit=True, background=False, border=False, **kwargs
                )

class GetKeyBox(TextBox):
    def __init__(self, game, text, **kwargs):
        super(GetKeyBox, self).__init__(
                game, text, textfit=True, background=True, border=True, xcenter=True, ycenter=True, **kwargs
                )
        self.value = None

    def eventHandler(self, event):
        if event.type == KEYDOWN:
            self.value = event.key
            self.update_required = False
            self.draw_required = False
            self.game.lock[KEYDOWN] = self

class ScrollingText(AutoTextBox):
    def __init__(self, game, text, speed=1, **kwargs):
        super(ScrollingText, self).__init__(game, text, **kwargs)
        if speed > 0:
            self.y = -(self.height)
        elif speed < 0:
            self.y = self.game.height
        else:
            raise TypeError("Scrolling speed must be non-zero")
        self.speed = speed

    def update(self):
        super(ScrollingText, self).update()

        if (self.y >= self.game.height and self.speed > 0) or (self.y + self.height <= 0 and self.speed < 0):
            self.update_required = False
            return

        self.y += self.speed

class Notification(TextBox):
    def __init__(self, game, _id, text):
        super(Notification, self).__init__(
                game, text, xcenter=True, ycenter=True, font=ERRORBOX_FONT,
                textfit=True, onmouseclick=lambda: game.removeJob(_id),
                colors=ERRORBOX_COLORSCHEME, background=True, border=True,
                )

class Board(object):
    def __init__(self, screen, x=0, y=0, blockwidth=0, width=0, height=0, bgcolor=(0x3f,0x3f,0x3f),
                 innercolor=(0x3F,0x3F,0x3F), outercolor=(0x50,0x50,0x50), queue=Queue.BOARD, level=1, draw_grid=True,
                ):
        self.anchor = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.blocks = {}
        self.drawncubes = set()
        self.blockwidth = blockwidth
        self.screen = screen
        self.bgcolor = bgcolor
        self.innercolor = innercolor
        self.outercolor = outercolor
        self.isupdated = True
        self.update_required = True
        self.draw_required = True
        self.state = ""
        self.queue = queue
        self.level = level
        self.score = 0
        self.lines = 0
        self.level_lines = LEVEL_LINES + ((self.level-1) * LEVEL_LINES_INCREASE)
        self.draw_grid = draw_grid
        self.force_draw = True

        ## XXX: Currently does not support filling, because the width and height
        ##      are in BOARD_BLOCKWIDTH.
        self.fill = False

    def drawCube(self, x, y, color):
        if y < 0:
            return

        Pygame.draw.rect(
                self.screen,
                color,
                (self.x + x*self.blockwidth + 1, self.y + y*self.blockwidth + 1, self.blockwidth - 1, self.blockwidth - 1)
                )

        self.drawncubes.add((x, y))

    ## TODO: The unexpected-ghost-bug occurs in here
    ##       the bug occurs when you have a block higher than all the others,
    ##       and then "get" a row.
    def checkTetris(self, rows=None):
        if rows == None:
            rows = xrange(self.height)

        lines = 0

        for row in rows:
            points = [p for p in self.blocks if p[1] == row]
            if len(points) == self.width:
                lines += 1
                for p in points:
                    self.blocks.pop(p)
                new_blocks = {}
                for x, y in self.blocks:
                    if y < row:
                        new_blocks[(x, y+1)] = self.blocks[(x, y)]
                    else:
                        new_blocks[(x, y)] = self.blocks[(x, y)]
                self.blocks = new_blocks

        if lines:
            ## XXX: Temporary bugfix for the unexpected-ghost-bug, re-draw everything when
            ##      the player gets one or more lines.
            self.force_draw = True
            self.score += SCORES["tetris"].get(lines, 9001)

        self.lines += lines

        self.level_lines -= lines

        if self.level_lines <= 0:
            self.level += 1
            self.level_lines = LEVEL_LINES + (LEVEL_LINES_INCREASE * (self.level-1)) - self.level_lines

    def update(self):
        self.isupdated = True

    def draw(self):
        if self.force_draw:
            self.drawBoard()

        ## Store the blocks that are currently drawn for later use
        oldblocks = self.drawncubes
        ## Draw the new blocks
        if self.force_draw:
            self.drawAllBlocks()
        else:
            self.drawNewBlocks()
            self.emptyBlocks(oldblocks.difference(self.blocks))
        ## Empty out the blocks that where drawn last time, but are no longer occupied
        self.isupdated = False
        self.force_draw = False

    def emptyBlocks(self, blocks):
        for x, y in blocks:
            self.drawCube(x, y, self.bgcolor)
            self.drawncubes.discard((x, y))

    ## TODO: Switch to this method, drawing every single block each time is a waste
    ##       of resources. Just need to figure some more stuff out.
    def drawNewBlocks(self):
        for block in self.drawncubes.difference(self.blocks):
            if self.blocks.get(block):
                self.drawCube(block[0], block[1], self.blocks[block])

    def drawAllBlocks(self):
        for block in self.blocks:
            self.drawCube(block[0], block[1], self.blocks[block])

    def drawBoard(self):
        """ Yup, just draw the board """

        Pygame.draw.rect(
                self.screen,
                self.outercolor,
                (self.x, self.y, (self.width * self.blockwidth) + 1, self.height * self.blockwidth + 1,),
                1)
        Pygame.draw.rect(
                self.screen,
                self.bgcolor,
                (self.x+1, self.y+1, self.width * self.blockwidth - 2, self.height * self.blockwidth - 1),
                0)
        if self.draw_grid:
            for x in xrange(1, self.width):
                Pygame.draw.line(
                        self.screen,
                        self.innercolor,
                        (self.x + self.blockwidth*x, self.y + 1),
                        (self.x + self.blockwidth*x, self.y + self.height*self.blockwidth - 2),
                        1)
            for y in xrange(1, self.height):
                Pygame.draw.line(
                        self.screen,
                        self.innercolor,
                        (self.x + 1, self.y + self.blockwidth*y),
                        (self.x + self.width*self.blockwidth - 2, self.y + self.blockwidth*y),
                        1)

    def getBlockInPos(self, x, y):
        """ Get the block coordinates for pixel coordinates
            used primarily to see which block the mouse is on
        """
        xpos = (x - self.x) / self.blockwidth
        ypos = (y - self.y) / self.blockwidth
        return xpos, ypos

    def eventHandler(self, event):
        pass

