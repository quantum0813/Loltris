#!/usr/bin/python2
#-*- coding: utf-8 -*--

## Tetris clone written in Python/Pygame, with some weird features.
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

import pygame as Pygame
import sys as Sys
import random as Random
import Queue
import Load
import Log
import Save
import os.path
from pygame.locals import *
from Exceptions import *
from xml.etree import ElementTree

tetrominos = None
keymap = None

## TODO: Add a highscore list, this is the most obvious feature at this point.

## TODO: Make it draw faster by limiting what is being drawn and update, work
##       on this has already been started.

## TODO: Add a sprite class to derive from, all the sprites I have thus far have a
##       a lot of things in common. It would also serve as a nice piece of documentation
##       for what a sprite (or object or whatever) should be able to do.

SCREEN_HEIGHT = 360
SCREEN_WIDTH = 360
FRAMERATE = 30
BLOCK_WIDTH = 10
BLOCK_HEIGHT = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 16
SOUND_ENABLED = False
HIGHSCORES = 10
UBERCOLOR = (0x70, 0x70, 0x22)

## TODO: Need a way to set this.
PLAYER = "Anon"

BOARD_BLOCKWIDTH = 20
LEVEL_LINES = 20
LEVEL_LINES_INCREASE = 5
UPDATEINTERVAL_DECREASE = FRAMERATE / 10

## TODO: XML this shit
GLOBAL_FONT_NAME = "monaco"
MENU_HEADER_FONT = {
        "name":"monaco",
        "size":40,
        "bold":True,
        }
MENU_OPTION_FONT = {
        "name":"monaco",
        "size":20,
        "bold":False,
        }
MENU_COLORSCHEME = {
        "header": (0xff,0xff,0xff),
        "selected": (0x66,0x66,0x66),
        "background":(0x22,0x22,0x22),
        "option":(0xaa,0xaa,0xaa),
                }
TETRIS_STATUSBOX_FONT = {
        "name":"monaco",
        "size":15,
        "bold":False,
        }

# DISPLAY_OPTIONS = FULLSCREEN | DOUBLEBUF | HWSURFACE
DISPLAY_OPTIONS = 0
GHOST_COLOR = (0x29, 0x29, 0x29)

SCORES = {
        "tetris": {1: 100, 2: 250, 3: 500, 4: 1500},
        }

globfonts = { }

def printTetromino(matrix, t="#", f=" "):
    """ Prints a matrix to the console for debugging purposes """
    for y in matrix:
        for x in y:
            Sys.stdout.write(t if x else f)
        print

def flip(matrix):
    for row in matrix:
        row.reverse()

## Because computing the next iteration is in this case better
## than storing all of them in order.
def rot90(matrix):
    xl, yl = len(matrix[0]), len(matrix)

    ret = []
    plane = []
    for x in xrange(xl):
        for y in xrange(yl-1, -1, -1):
            plane.append(matrix[y][x])
        ret.append(plane)
        plane = []

    return ret

## TODO: Finish this
class Job(object):
    def __init__(self):
        pass

class Tetromino(object):
    def __init__(self, board, matrix, _type, color, x=0, y=None, ghostpiece=True, updateinterval=FRAMERATE, queue=None):
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

        self.ghostpiece = None
        if ghostpiece:
            self.ghostpiece = GhostTetromino(board, matrix, _type, GHOST_COLOR, x=x, y=y)
            self.ghostpiece.drop()

        if y == None:
            self.y = -(len(self.matrix))

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
        self.matrix = rot90(self.matrix)
        if self.checkWallCollision(self.x, self.y) or self.checkBlockCollision():
            self.matrix = last_matrix
        else:
            self.updateGhost("rotate", direction)

    def updateGhost(self, attr, *args, **kwargs):
        if self.ghostpiece:
            self.ghostpiece.y = self.y
            self.ghostpiece.x = self.x
            getattr(self.ghostpiece, attr)(*args, **kwargs)
            self.ghostpiece.drop()

    ## It makes the game WAAY to easy, but i kind of always wondered "what if"
    def flip(self):
        flip(self.matrix)
        if self.checkWallCollision(self.x, self.y) or self.checkBlockCollision():
            flip(self.matrix)
        else:
            self.updateGhost("flip")

    def eventHandler(self, events):
        for event in events:
            if event.type == KEYUP:
                if event.key == keymap["game"]["speed_up"] and self.sped_up:
                    self.sped_up = False
                    self.updateinterval *= 10
                    self.time_until_update = self.updateinterval

            if event.type == KEYDOWN:
                if event.key == keymap["game"]["rotate_right"]:
                    self.rotate(1)
                elif event.key == keymap["game"]["rotate_left"]:
                    self.rotate(-1)
                elif event.key == keymap["game"]["reverse"]:
                    self.flip()

                elif event.key == keymap["game"]["move_right"]:
                    self.moveHorizontal(1)
                elif event.key == keymap["game"]["move_left"]:
                    self.moveHorizontal(-1)

                elif event.key == keymap["game"]["drop_down"]:
                    self.drop()

                elif event.key == keymap["game"]["speed_up"]:
                    self.sped_up = True
                    self.updateinterval /= 10
                    self.time_until_update = self.updateinterval

## This object will be managed by a Tetromino(), it should not be managed as a Job
class GhostTetromino(Tetromino):
    def __init__(self, *args, **kwargs):
        super(GhostTetromino, self).__init__(*args, ghostpiece=False, **kwargs)

    def drop(self):
        for y in xrange(self.board.height+1):
            self.y = y
            if self.checkBlockCollision() or self.checkWallCollision(self.x, self.y) == "bottom":
                self.y -= 1
                break

class Board(object):
    def __init__(self, screen, x=0, y=0, blockwidth=0, width=0, height=0, innercolor=(0x3F,0x3F,0x3F), outercolor=(0x50,0x50,0x50), queue=0, level=1):
        self.anchor = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.blocks = {}
        self.drawnblocks = set()
        self.blockwidth = blockwidth
        self.screen = screen
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

    def drawCube(self, x, y, color):
        if y < 0:
            return

        Pygame.draw.rect(
                self.screen,
                color,
                (self.x + x*self.blockwidth + 1, self.y + y*self.blockwidth + 1, self.blockwidth - 1, self.blockwidth - 1)
                )

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
            self.score += SCORES["tetris"].get(lines, 9001)
        self.lines += lines

        self.level_lines -= lines

        if self.level_lines <= 0:
            self.level += 1
            self.level_lines = LEVEL_LINES + (LEVEL_LINES_INCREASE * (self.level-1)) - self.level_lines

    def update(self):
        self.isupdated = True

    def draw(self):
        self.drawAllBlocks()
        self.drawBoard()
        self.isupdated = False

    ## TODO: Switch to this method, drawing every single block each time is a waste
    ##       of resources. Just need to figure some more stuff out.
    def drawNewBlocks(self):
        for block in self.drawnblocks.difference(self.blocks):
            self.drawCube(block[0], block[1], self.blocks[block])
            self.drawnblocks.add(block)

    def drawAllBlocks(self):
        for block in self.blocks:
            self.drawCube(block[0], block[1], self.blocks[block])

    def drawBoard(self):
        """ Yup, just draw the board """

        Pygame.draw.rect(
                self.screen,
                self.outercolor,
                (self.x, self.y, self.width * self.blockwidth, self.height * self.blockwidth + 1),
                1)
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

    def eventHandler(self, events):
        pass

class Jobs(object):
    def __init__(self):
        pass

class Game(object):
    def __init__(self, _id, caption="", mouse_visible=True, bgcolor=(0x22,0x22,0x22), screen=None, ticktime=FRAMERATE,
                 width=SCREEN_WIDTH, height=SCREEN_HEIGHT, x=SCREEN_WIDTH, y=SCREEN_HEIGHT, sound_enabled=False, soundtrack=None):
        Log.log("Initializing Game object `{}'".format(_id))
        self.jobs = Jobs()
        self.caption = caption
        self.mouse_visible = mouse_visible
        self.bgcolor = bgcolor
        self.screen = screen
        self.ticktime = ticktime
        self.ret = 0
        self.windows = {}
        self.height = y
        self.width = x
        self.events = None
        self.id = _id
        self.soundtrack = soundtrack
        self.sound_enabled = sound_enabled
        self.playing = ""

        self.setup()

    def stopMusic(self):
        self.playing = ""
        Pygame.mixer.music.stop()

    ## TODO: The call/quit model currently fails here, I'll just have to save the music's "progress."
    def playMusic(self, path, loops=1):
        try:
            if not self.sound_enabled:
                Log.warning("Attempted to play music in `{}' where sound has been disabled".format(self.id))
            Pygame.mixer.music.load(path)
            Pygame.mixer.music.play(loops)
            Log.log("Playing sountrack `{}'".format(path))
            self.playing = path
        except:
            Log.error("Unable to play music file: `{}'".format(path))

    def getJob(self, name):
        return getattr(self.jobs, name)

    def addJob(self, name, obj):
        setattr(self.jobs, name, obj)

    ## Why not just call Sys.exit(), why create a separate method for this?
    ## Because finishing of can get more complex as this program develops.
    def quit(self):
        Sys.exit()

    ## We just "exploit" the stack to create things like pause menus or other "contexts"
    ## that take over the screen.
    def call(self, obj, **kwargs):
        game = obj(screen=self.screen, **kwargs)
        ret = game.run()

        self.setup()

        if ret and self.id != ret:
            self.quitGame(ret)

    def quitGame(self, *args):
        if args:
            self.ret = args[0]
        if self.playing:
            self.stopMusic()
        self.running = None

    def setup(self):
        Pygame.init()
        Pygame.display.set_caption(self.caption)
        Pygame.mouse.set_visible(int(self.mouse_visible))
        if not Pygame.mixer.get_init() and self.sound_enabled:
            Log.log("Initializing mixer")
            Pygame.mixer.init()
        if self.soundtrack and self.sound_enabled and not self.playing:
            self.playMusic(self.soundtrack, loops=-1)
        if not self.screen:
            self.screen = Pygame.display.set_mode((self.width, self.height), DISPLAY_OPTIONS)
        self.screen.fill(self.bgcolor)
        Pygame.display.flip()
        self.clock = Pygame.time.Clock()

    def eventHandler(self, events):
        pass

    def run(self):
        if not hasattr(self, "running") or not hasattr(self, "eventHandler"):
            raise GameError("Game has not been properly initialized")

        while self.running:
            self.clock.tick(self.ticktime)
            self.screen.fill(self.bgcolor)
            self.events = Pygame.event.get()
            queue = sorted(self.jobs.__dict__, key=lambda obj: getattr(self.jobs, obj).queue)
            for obj in queue:
                obj = self.getJob(obj)
                if obj.update_required:
                    obj.update()
                if obj.draw_required:
                    obj.draw()

                ## Context is love, context is life.
                obj.eventHandler(self.events)
            Pygame.display.flip()
            self.eventHandler(self.events)
            if self.running:
                self.running()

        return self.ret

## Creates a perfect tetromino (for the current board)
def makeUberTetromino(board):
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
    return Tetromino(board, tetromino, "UBER", UBERCOLOR, x=0)

def randomTetromino(board, updateinterval=FRAMERATE/2):
    color, type, matrix = Random.choice(tetrominos)
    return Tetromino(board, matrix, type, color, x=(board.width/2)-1, updateinterval=updateinterval)

def genKey(d):
    """
    >>> genKey({"name": "GenericFont", "size": 40, "bold": True})
    'TrueGenericFont40'
    """
    return "".join([str(d[key]) for key in sorted(d)])

class TextBox(object):
    def __init__(self, game, text, colors={"background": (0,0,0)}, border=False, ycenter=False, underline=False, background=False,
                 xcenter=False, x=0, y=0, height=0, width=0, textfit=False, font={"name": ""}, padding=12, queue=None, variables={},
                 updatewhen=None):
        Log.log("Initializing TextBox for `{}' with {}".format(
            game.id, repr(text) if len(repr(text)) < 20 else repr(text)[:17]+"...'"))
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
        self.colors = colors
        self.textfit = textfit
        self.ycenter = ycenter
        self.xcenter = xcenter
        self.padding = padding
        self.variables = variables

        ## XXX: Hold that thought
        self.updatewhen = updatewhen

        self.renderFonts()

    def renderFonts(self):
        variables = {}
        for var in self.variables:
            variables[var] = self.variables[var](self.game)
        text = self.text.format(**variables)

        if not self.font.get("name"):
            self.font["name"] = Pygame.font.get_default_font()
        fontobj = globfonts.get(genKey(self.font))
        if not fontobj:
            fontobj = globfonts[genKey(self.font)] = \
                    Pygame.font.SysFont(self.font["name"], self.font.get("size", 40), bold=self.font.get("bold"), italic=self.font.get("italic"))

        self.rendered_fonts = []
        self.fontwidth = 0
        self.fontheight = 0
        for line in text.splitlines():
            self.rendered_fonts.append(fontobj.render(line.rstrip("\n"), True, self.colors["font"]))
            width, height = fontobj.size(line)
            self.fontwidth = self.fontwidth if self.fontwidth > width else width
        self.fontheight = height

        if self.textfit:
            self.width, self.height = self.fontwidth, self.fontheight*len(self.rendered_fonts)
            self.xpadding = (self.width/self.padding)
            self.width += self.xpadding
            self.ypadding = (self.height/self.padding)
            self.height += self.ypadding

        if self.xcenter:
            self.x = (self.game.width / 2) - (self.width / 2)
        if self.ycenter:
            self.y = (self.game.height / 2) - (height / 2)

    def draw(self):
        ## XXX: Hold that thought
        if self.updatewhen:
            for update in updatewhen:
                pass

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

    def eventHandler(self, events):
        pass

    def update(self):
        pass

## TODO: Add sliders and other fancy shit
class Menu(Game):
    def __init__(self, _id, header_font={"size":60, "bold":False}, option_font={"size":60, "bold":False}, decorate_options=False, **kwargs):
        self.id = _id
        super(Menu, self).__init__(self.id, **kwargs)
        self.running = self.mainLoop
        self.colorscheme = MENU_COLORSCHEME
        self.header = ""
        self.menu = {}
        self.options = []
        self.selected = 0
        self.options_pos = (10, 80)
        self.header_font = header_font
        self.option_font = option_font

    def setupObjects(self):
        self.addJob("header",
                TextBox(self, self.header, y=20, xcenter=True, textfit=True, underline=True,
                    colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)}, font=self.header_font,
                    )
                )
        x, y = self.options_pos
        self.options = []
        for option in self.menu:
            # option = option.replace(" ", "_")
            self.options.append("{}".format(option))
            self.addJob("{}".format(option),
                    TextBox(self, option, y=y, x=x, textfit=True,
                        colors={
                            "background":self.colorscheme["background"],
                            "font":self.colorscheme["selected"] if len(self.options)-1==self.selected else self.colorscheme["option"]
                            },
                        font=self.option_font,
                        )
                    )
            y += self.getJob("{}".format(option)).fontheight

    def mainLoop(self):
        pass

    def changeMenu(self, menu):
        self.call(menu)

    def close(self):
        self.quitGame()

    def moveUp(self):
        if self.selected == 0:
            self.selected = len(self.options)-1
        else:
            self.selected -= 1
        self.setupObjects()

    def moveDown(self):
        if self.selected == len(self.options)-1:
            self.selected = 0
        else:
            self.selected += 1
        self.setupObjects()

    def execOption(self):
        ## Right now each option just runs a function, this may change
        option = self.menu[self.options[self.selected]]
        option()

    def eventHandler(self, events):
        for event in events:
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                if event.key == keymap["menu"]["back"]:
                    self.close()
                elif event.key == keymap["menu"]["down"]:
                    self.moveDown()
                elif event.key == keymap["menu"]["up"]:
                    self.moveUp()
                elif event.key == keymap["menu"]["select"]:
                    self.execOption()

class TimedExecution(object):
    def __init__(self, function, cycles=0, seconds=0, anykey=True):
        self.update_required = True
        self.draw_required = False
        self.queue = 0
        self.anykey = True
        self.function = function

        if cycles:
            self.cycles = cycles
        elif seconds:
            self.cycles = seconds * FRAMERATE

    def eventHandler(self, events):
        for event in events:
            if event.type == KEYDOWN and self.anykey:
                self.update_required = False
                self.function()

    def draw(self):
        pass

    def update(self):
        if self.cycles <= 0:
            self.update_required = False
            self.function()
        self.cycles -= 1

class TetrisGame(Game):
    def __init__(self, player_name="", *args, **kwargs):
        self.id = "TetrisGame"
        super(TetrisGame, self).__init__(self.id, *args, soundtrack=os.path.join(Load.MUSICDIR, "uprising.mp3"), sound_enabled=SOUND_ENABLED, **kwargs)
        self.running = self.mainLoop
        self.highscores = Load.loadHighscores(top=HIGHSCORES)
        self.player_name = player_name

        ## All the jobs
        self.addJob("board", Board(self.screen, x=BLOCK_WIDTH, y=BLOCK_HEIGHT, height=BOARD_HEIGHT, width=BOARD_WIDTH, blockwidth=BOARD_BLOCKWIDTH, level=kwargs.get("level", 1)))
        self.addJob("tetromino", randomTetromino(self.jobs.board, updateinterval=FRAMERATE - (self.getJob("board").level-1)*UPDATEINTERVAL_DECREASE))
        self.addJob("status",
                TextBox(self, "Level: {level}\nScore: {score}\nLines: {lines}\nLines left: {level up}", border=True, y=BLOCK_HEIGHT+1, x=BLOCK_WIDTH*2+(BOARD_WIDTH)*BOARD_BLOCKWIDTH, textfit=True,
                    colors={"border":(0xaa,0xaa,0xaa), "font":(0xaa,0xaa,0xaa)},
                    font=TETRIS_STATUSBOX_FONT,
                    variables={
                        "level": lambda s: s.getJob("board").level,
                        "score": lambda s: s.getJob("board").score,
                        "lines": lambda s: s.getJob("board").lines,
                        "level up": lambda s: s.getJob("board").level_lines,
                        }
                    )
                )

    def mainLoop(self):
        if not self.getJob("board").update_required and not hasattr(self.jobs, "window-game_over"):
            ## XXX: GAME OVER
            board = self.getJob("board")
            if len(self.highscores) < HIGHSCORES or any(board.score > score for score in self.highscores):
                self.addJob("window-game_over",
                            TextBox(self, "New Highscore!", border=True, ycenter=True, xcenter=True, width=80, height=50, textfit=True, background=True,
                                colors={"background":(0x22,0x22,0x22), "border":(0xaa,0xaa,0xaa), "font":(0x66,0x66,0x66)},
                                font={ "name":"monaco", "size":35, "bold":False }
                                )
                            )
                Save.saveScores([{"name": self.player_name, "score": board.score, "level": board.level, "lines": board.lines}])
            else:
                self.addJob("window-game_over",
                            TextBox(self, "Game Over", border=True, ycenter=True, xcenter=True, width=80, height=50, textfit=True, background=True,
                                colors={"background":(0x22,0x22,0x22), "border":(0xaa,0xaa,0xaa), "font":(0xaa,0x22,0x22)},
                                font={ "name":"monaco", "size":35, "bold":True }
                                )
                            )
            self.addJob("endtimer", TimedExecution(self.quitGame, seconds=2, anykey=True))

        if not self.jobs.tetromino.update_required and self.getJob("board").update_required:
            self.addJob("tetromino", randomTetromino(self.jobs.board, updateinterval=FRAMERATE - (self.getJob("board").level-1)*UPDATEINTERVAL_DECREASE))

    def eventHandler(self, events):
        if not events:
            return

        for event in events:
            if event.type == QUIT:
                self.quit()

            elif event.type == KEYDOWN:
                if event.key == keymap["game"]["pause"]:
                    self.call(PauseMenu, caption="Tetris - Paused")

                if event.key == keymap["game"]["uber_tetromino"]:
                    self.addJob("tetromino", makeUberTetromino(self.getJob("board")))


## Placeholder, need to add sliders and other stuff to the Menu class
## for an option menu to be doable.
class OptionsMenu(Menu):
    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__("OptionsMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
        self.header = "Options"
        self.menu = {
                "Crash": lambda: lololololololololol
                }
        self.setupObjects()

class MainMenu(Menu):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__("MainMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
        self.header = "Loltris"
        self.menu = {
                "Start Game": self.startTetrisGame,
                "Options": lambda: self.call(OptionsMenu, caption="Loltris - options"),
                "Quit": self.quit,
                }
        self.setupObjects()
        # self.addJob(
        #          "HighscoreList",
        #          TextBox(self, option, y=y, x=x, textfit=True,
        #              colors={
        #                  "background":self.colorscheme["background"],
        #                  "font":self.colorscheme["selected"] if len(self.options)-1==self.selected else self.colorscheme["option"]
        #                  },
        #              font=self.option_font,
        #              )
        #         )

    def startTetrisGame(self):
        self.call(TetrisGame, caption="Loltris", player_name=PLAYER)

class PauseMenu(Menu):
    def __init__(self, **kwargs):
        super(PauseMenu, self).__init__("PauseMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
        self.header = "Pause"
        self.menu = {
                "Quit Game": self.quit,
                "Quit to main menu": lambda: self.quitGame("MainMenu"),
                "Continue": self.quitGame,
                }
        self.setupObjects()

class MakeTetromino(Game):
    def __init__(self, *args, **kwargs):
        self.id = "MakeTetromino"
        super(TetrisGame, self).__init__(self.id, *args, sound_enabled=SOUND_ENABLED, **kwargs)
        ## TODO: The user should be able to change this
        self.color = (0xbb,0xbb,0xbb)
        self.addJob(
                "board",
                Board(self.screen,
                      x=BLOCK_WIDTH,
                      y=BLOCK_HEIGHT,
                      height=BOARD_HEIGHT,
                      width=BOARD_WIDTH,
                      blockwidth=BOARD_BLOCKWIDTH,
                      level=kwargs.get("level", 1)
                      ),
                )

    def eventHandler(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                x, y = self.jobs.board.getBlockInPos(Pygame.mouse.get_pos())
                self.jobs.blocks[(x, y)] = self.color

    def save(self):
        pass

if __name__ == '__main__':
    import doctest
    tetrominos = Load.loadTetrominos()
    keymap = Load.loadKeymaps()
    doctest.testmod()
    MainMenu(caption="Loltris").run()
