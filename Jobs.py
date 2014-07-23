#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## All the jobs (or game objects) used in Game derived instances
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

## TODO: This file should be modularized

import pygame as Pygame
import Queue
import Load
import Log
import Utils
import Shared
import Matrix
import RGB
import Draw
import os.path as path
from pygame.locals import *
from Globals import *
from DataTypes import *
from Hacks import *

class Job(object):
    """
    The basic structure of a job, all required attributes and methods.
    """
    def __init__(self, game, x, y, queue=Queue.GENERIC, bgcolor=(0x22,0x22,0x22)):
        self.game = game
        self.x = x
        self.y = y
        self.force_draw = True
        self.queue = queue
        self.update_required = True
        self.draw_required = True
        self.handling_events = True
        self.fill = False
        self.resize = False
        self.keydownhandlers = {}
        self.keyuphandlers = {}
        self.bgcolor = bgcolor
        ## Jobs are recursive datatypes, they may have other jobs running "underneath"
        self.jobs = Struct()
        self.screen = self.game.screen

    def getJob(self, name):
        return getattr(self.jobs, name)

    def addJob(self, name, obj):
        setattr(self.jobs, name, obj)

    def runSubs(self):

        ## The events and updates should be handled in reverse order (the things on top go first)
        queue = sorted(self.jobs.__dict__, key=lambda obj: getattr(self.jobs, obj).queue, reverse=True)
        for objname in queue:
            if objname not in self.jobs.__dict__:
                ## In case a Job modifies self.jobs, removing this job.
                continue

            obj = self.getJob(objname)
            ## XXX: This second check of update_required is necessarry because eventHandler() may either modify
            ##      or call methods that modify parameters in obj.
            if obj.update_required:
                obj.update()

        queue = sorted(self.jobs.__dict__, key=lambda obj: getattr(self.jobs, obj).queue)
        ## Handle resizing (redraw everything underneath the resized job)
        for objname in queue:
            obj = self.getJob(objname)
            if obj.__dict__.get("resize"):
                for job in self.getJobsIn(objname):
                    job.force_draw = True
                obj.resize = False

        ## Unlike the events and updates, drawing is handled so that the lowest go first
        for objname in queue:

            if objname not in self.jobs.__dict__:
                ## In case a Job modifies self.jobs, removing this job.
                continue

            obj = self.getJob(objname)

            if objname not in self.jobs.__dict__:
                ## In case a Job modifies self.jobs, removing itself during update.
                continue

            if obj.draw_required:
                if obj.fill:
                    Draw.fillJob(self.screen, obj.fill, obj)
                obj.draw()

        ## Remove locks
        self.lock = {}

    def draw(self):
        self.force_draw = False

    def runSubEventHandlers(self, event):
        for job in self.jobs:
            if self.jobs[job].update_required and self.jobs[job].handling_events:
                self.jobs[job].eventHandler(event)

    def eventHandler(self, event):
        if event.type == KEYDOWN and self.keydownhandlers.get(event.key):
            self.keydownhandlers[event.key](event)
        elif event.type == KEYUP and self.keyuphandlers.get(event.key):
            self.keyuphandlers[event.key](event)
        elif event.type == MOUSEMOTION and hasattr(self, "mouseMotionHandler"):
            self.mouseMotionHandler(event)
        elif event.type == MOUSEBUTTONDOWN and hasattr(self, "mouseButtonDownHandler"):
            self.mouseButtonDownHandler(event)
        elif event.type == MOUSEBUTTONUP and hasattr(self, "mouseButtonUpHandler"):
            self.mouseButtonUpHandler(event)
        if self.jobs:
            self.runSubEventHandlers(event)

    def update(self):
        if self.force_draw:
            for job in self.jobs:
                self.jobs.__dict__[job].force_draw = True

        if self.jobs:
            self.runSubs()

## TODO: Jobs.py might not be the most logical place for this, move this to
##       a more suitable module.
def loadFont(font):
    if not font.get("name"):
        font["name"] = Pygame.font.get_default_font()
    fontobj = Shared.fonts.get(Utils.genKey(font))
    if not fontobj:
        try:
            fontobj = Shared.fonts[Utils.genKey(font)] = \
                    Pygame.font.Font(
                            path.join(Load.TTF_FONTDIR, "{}.ttf".format(font["name"])),
                            font.get("size", 40),
                            bold=font.get("bold"),
                            italic=font.get("italic")
                            )
        except IOError:
            Log.panic("Unable to load font: `{}'".format(font["name"]))
    return fontobj

class ColorPalette(Job):
    """
    Job for mixing together values into a color, using sliders.
    """
    def __init__(self, game, x, y, window_width, width=10):
        assert window_width > SPACER*2, "Window width is too small for spacers"

        super(ColorPalette, self).__init__(game, x, y)

        self.red = 0
        # self.red_slider = Slider((x + SPACER, y), (x + window_width - SPACER, y), width=width, colors=)
        self.green = 0
        self.blue = 0
        # self.sliders = Factory.sliders

    def value(self):
        return (self.red, self.green, self.blue)

    def drawLines(self):
        pass

    def drawSliders(self):
        for slider in sliders:
            slider.draw()

    def draw(self):
        self.drawLines()
        self.drawSliders()
        self.force_draw = False

    def eventHandler(self, event):
        if event.type == MOUSEBUTTONDOWN:
            pass

## TODO: Add markup, to allow for different fonts in different parts of the same textbox
## XML Examples:
"""
<font size="40" style="bold" name="Arial">Title</font>
<font size="20" style="cursive" name="Times New Roman">Something, something, something</font>
"""
## TODO: Could also just use built-in datatypes, i.e a list of dictionaries
## Examples:
"""
[
    {
        "font": "Arial",
        "text": "Title",
        "bold": true,
        "size": 40,
    },
    {
        "font": "Times New Roman",
        "text": "Something, something, something",
        "size": 20,
        "cursive": true,
    },
]
"""
class TextBox(Job):
    """
    Multi-purpose text-box, takes the following keyword arguments:

    onmouseclick (func):
        Info:
            A function activated when the mouse is clicked while inside the TextBox object.
            This function is not given any arguments.
        Default:
            None

    onmouseenter (func):
        Info
            A function activated when the mouse is moved inside the TextBox (from outside of it.)
            This function is given one argument, the TextBox it belongs to. Example below
            def onmouseenter(textbox_object):
                ...
        Default:
            None

    onmouseleave (func):
        Info
            A function activated when the mouse is moved outside the TextBox (from inside of it.)
            This function is given one argument, the TextBox it belongs to. Example below
            def onmouseleave(textbox_object):
                ...
        Default:
            None

    variables (dict):
        Info:
            A dictionary. Will be used like this on the TextBox's text:
            text.format(**variables)
            this is how a TextBox can handle text that changes.
        Default:
            {}

    xcenter (bool):
        Info:
            Centers the textbox along the width of the screen.
        Default:
            False

    ycenter (bool):
        Info:
            Centers the textbox along the height of the screen.
        Default:
            False

    underline (bool):
        Info:
            Draw a line underneath the text.
        Default:
            False

    colors (dict):
        Info:
            Colors of different parts of the TextBox, given as tuples with three values
        Default:
            {"background": (0,0,0)}

    background (bool):
        Info:
            Draw a background with the color colors["background"]
        Default:
            False

    border (bool):
        Info:
            Draw a border with the color colors["border"] around the TextBox
        Default:
            False

    font (dict):
        Info:
            Controls the font used
        Default:
            {"name": ""}

    yfit (bool):
        Info:
            Fit the height according to the fonts. Constant height given as keyword "height" will be ignored.
        Default:
            False

    xfit (bool):
        Info:
            Fit the width according to the fonts. Constant width given as keyword "width" will be ignored.
        Default:
            False

    textfit (bool):
        Info:
            LEGACY, has been replaced by xfit and yfit
            Same as xfit=True and yfit=True.
        Default:
            False

    padding (int):
        Info:
            The TextBox will be padded with the width/height divided by padding.
        Default:
            12

    height (int):
        Info:
            Set height manually with a constant int.
        Default:
            0

    width (int):
        Info:
            Set width manually with a constant int.
        Default:
            0

    x (int):
        Info:
            x coordinate
        Default:
            0

    y (int):
        Info:
            y coordinate
        Default:
            0

    border_width (int):
        Info:
            Controls width of the border in pixels. (if the border has been enabled with border=True)
        Default:
            1
    """
    def __init__(self, game, text, colors={"background": (0,0,0)}, border=False, ycenter=False, underline=False, background=False,
                 xcenter=False, x=0, y=0, height=0, width=0, textfit=False, yfit=False, xfit=False, font={"name": ""}, padding=12,
                 queue=None, variables={}, onmouseclick=None, onmouseenter=None, onmouseleave=None, fill=FALLBACK_COLOR,
                 border_width=1):

        super(TextBox, self).__init__(game, x, y)

        assert text, "Empty string given to TextBox"

        self.game = game
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border = border
        self.colors = copy(colors)
        self.update_required = True
        self.draw_required = True
        self.xpadding = 0
        self.ypadding = 0
        self.underline = underline
        self.background = background
        self.queue = queue if queue != None else Queue.TEXTBOX
        self.text = text
        self.font = copy(font)
        self.textfit = textfit
        self.ycenter = ycenter
        self.xcenter = xcenter
        self.padding = padding
        self.variables = variables
        self.fill = fill
        self.xfit = xfit
        self.yfit = yfit
        self.last_variables = {}
        self.border_width = border_width

        ## Mouse-related business
        self.onmouseclick = onmouseclick
        self.onmouseenter = onmouseenter
        self.onmouseleave = onmouseleave
        self.hasmouse = False

        if variables:
            self.update()
        else:
            self.filled_text = text

        self.renderFonts()

        self.colors = copy(colors)

    def renderFonts(self):
        if not self.font.get("name"):
            self.font["name"] = FALLBACK_FONT_NAME
        fontobj = Shared.fonts.get(Utils.genKey(self.font))
        if not fontobj:
            try:
                fontobj = Shared.fonts[Utils.genKey(self.font)] = \
                        Pygame.font.Font(
                            path.join(Load.TTF_FONTDIR, "{}.ttf".format(self.font["name"])),
                            self.font.get("size", 40),
                            bold=self.font.get("bold"),
                            italic=self.font.get("italic")
                        )
            except IOError:
                Log.panic("Unable to load font: `{}' for {}".format(self.font["name"], self))

        self.rendered_fonts = []
        self.fontwidth = 0
        self.fontheight = 0
        for line in self.filled_text.splitlines():
            self.rendered_fonts.append(fontobj.render(line.rstrip("\n"), True, self.colors["font"]))
            width, height = fontobj.size(line)
            self.fontwidth = self.fontwidth if self.fontwidth > width else width
        self.fontheight = height

        if self.textfit:
            ## XXX: LEGACY, textfit was used before xfit and yfit were introduced, textfit now implies
            ##      yfit and xfit.
            self.yfit = True
            self.xfit = True

        if self.xfit:
            self.width = self.fontwidth
            if self.padding:
                self.xpadding = (self.width/self.padding) if self.padding else 0
            self.width += self.xpadding
        if self.yfit:
            self.height = self.fontheight*len(self.rendered_fonts)
            self.ypadding = (self.height/self.padding) if self.padding else 0
            self.height += self.ypadding

        if self.xcenter:
            self.x = (self.game.width // 2) - (self.width // 2)
        if self.ycenter:
            self.y = (self.game.height // 2) - (self.height // 2)

    def draw(self):

        if self.background and self.fill:
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
                    (self.x-self.border_width, self.y-self.border_width,
                     self.width+self.border_width, self.height+self.border_width),
                    self.border_width,
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

    def fillArea(self, color):
        Pygame.draw.rect(
                self.game.screen,
                color,
                (self.x-self.border_width, self.y-self.border_width,
                 self.width+self.border_width + 1, self.height+self.border_width + 1),
                0)

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
            ## TODO: Maybe there should be a different event registered for button 1 and 3?
            if event.button in (1, 3):
                ## If the button pressed was either the left or right button
                if Utils.isInCube(Pygame.mouse.get_pos(), (self.x, self.y, self.width, self.height)):
                    Log.debug("Mouseclick on `{}'".format(self))
                    self.onmouseclick()
                    self.game.lock[MOUSEBUTTONDOWN] = self

    def update(self):
        if self.variables:
            variables = {}
            ## Generate new variables hash
            for var in self.variables:
                variables[var] = self.variables[var](self.game)
            text = self.text.format(**variables)

            ## Check if an update is required
            if variables != self.last_variables:
                Log.debug("Rendering fonts in TextBox `{}' variables have changed".format(self))
                self.filled_text = text
                self.renderFonts()
                self.last_variables = variables

class Slider(Job):
    """
    A slider, made so that start position and the and position can be anywhere as long as
    x0 <= x1 and y0 <= y1.
    """
    def __init__(self, game, from_pos, to_pos, width=10, colors=None, font=None, text=None):
        assert from_pos[0] <= to_pos[0]
        assert from_pos[1] <= to_pos[1]

        super(Slider, self).__init__(
            game, text, from_pos[0], from_pos[1]
        )

        if colors:
            self.colors = copy(colors)
        else:
            self.colors = {
                "background": (0,0,0),
                "filled": (0,0,0),
                "empty": (255,255,255),
                "slider": (0,0,0),
                "font": (255,255,255),
            }

        ## Misc. variables
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.frac = 0
        self.force_draw = True
        self.width = width
        self.text = text

        ## TextBox (for displaying the explanatory text)
        if text:
            assert font, "Text was given, but no font was given"
            self.textbox = AutoTextBox(self.game, text, x=from_pos[0], y=from_pos[1], font=font, colors=self.colors)
            self.textbox.y -= self.textbox.height

    def isIn(self, x, y):
        """
        Find out if the given coordinates are inside of the sliders' clickable area.
        """

        ## More readable names for the coordinates
        x0, y0 = self.from_pos
        x1, y1 = self.to_pos

        ## Distance between the points, on the y and x axis
        ydist = y0 - y1
        xdist = x0 - x1

        ## Equation for the line
        slope = float(ydist) / float(xdist)
        f = lambda x: y0 + x*slope

        ## Check x and y
        is_in_x = x0 <= x <= x1
        is_in_y = y - self.width <= f(x) <= y + self.width

        ## The coordinates are inside, if the x-coordinate is inside the x-axis,
        ## and the y-coordinate is inside the y-axis.
        return is_in_y and is_in_x

    def getFraction(self, x, y):
        """
        Get the percentage, on a specific (x, y) coordinate.
        """
        x0 = self.from_pos[0]
        x1 = self.to_pos[0]
        ## Derived from getMiddle
        percentage = abs(float(x - x0) / (x0 - x1))
        if percentage >= 1:
            return 1.0
        if percentage <= 0:
            return 0.0
        return percentage

    def getMiddle(self):
        x0, y0 = self.from_pos
        x1, y1 = self.to_pos
        ydist = y0 - y1
        xdist = x0 - x1
        return (x0 - xdist + (xdist * self.frac), y0 - ydist + (ydist * self.frac))

    def drawLine(self):
        filled_to_pos = self.getMiddle()

        Pygame.draw.line(
                self.game.screen,
                self.colors["empty"],
                filled_to_pos,
                self.to_pos,
                self.width
                )
        Pygame.draw.line(
                self.game.screen,
                self.colors["filled"],
                self.from_pos,
                filled_to_pos,
                self.width
                )

    def getValue(self):
        ## The fraction has to be "reversed"
        val = 1.0 - self.frac

        ## We must be certain that 0.0 <= val <= 1.0
        if val <= 0.0:
            return 0.0
        if val >= 1.0:
            return 1.0
        return val

    def increase(self, amount):
        ## This won't ever make sense, so if this happens it is most likely the result of an
        ## error higher up on the stack.
        assert -1.0 <= amount <= 1.0, "Increase may not exceed 1.0, or deceed -1.0"

        Log.debug("Increase {}.frac by {}".format(self, amount))
        self.force_draw = True
        if self.frac + amount >= 1:
            self.frac = 1.0
        elif self.frac + amount <= 0:
            self.frac = 0.0
        else:
            self.frac += amount
        Log.debug("{}.frac = {}".format(self, self.frac))

    def eventHandler(self, event):
        if event.type == MOUSEBUTTONDOWN:
            ## Left or right mouse button
            x, y = Pygame.mouse.get_pos()
            if self.isIn(x, y):
                Log.debug("Clicked inside {}".format(self))
                if event.button in (1, 3):
                    frac = self.getFraction(x, y)
                    self.frac = 1 - frac
                    self.force_draw = True
                if event.button == 4:
                    self.increase(-0.1)
                if event.button == 5:
                    self.increase(0.1)

    def drawText(self):
        if self.text:
            self.textbox.draw()

    def draw(self):
        if self.force_draw:
            self.drawLine()
            self.drawText()
            self.force_draw = False

## TODO: Create VerticalSlider and HorizontalSlider from Slider
# class HorizontalSlider(Slider):
#     def __init__(self, game, text, )

class Flipper(TextBox):
    def __init__(self, game, title, options, x=0, y=0, height=5, width=0, colors=None):
        def onMouseEnter(box):
            box.colors["font"] = self.colors["option"]
            box.renderFonts()
        def onMouseLeave(box):
            box.colors["font"] = self.colors["selected"]
            box.renderFonts()
        self.option = 0
        self.title = title
        self.colors = copy(colors)

        super(Flipper, self).__init__(
                game, title + options[0], x=x, y=y, background=True, colors=colors,
                )

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
        self.box_center = box_center

        self.renderFonts()

    def renderFonts(self):
        super(Switch, self).renderFonts()

        if hasattr(self, "boxwidth"):
            self.boxwidth = self.height // 3
            if self.box_center:
                self.box_offset = (self.height // 2) - (self.boxwidth // 2)
                self.y_center = self.y + self.height // 2

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

class TimedExecution(Job):
    """
    Execute a function after a given time. The timing is handled in terms of cycles,
    i.e how many times update has been called. It is therefore dependant on the framerate
    being kept at a relatively constant speed. The time can be given in seconds or in
    cycles (seconds are recommended.)

    Takes the following keyword arguments:
    
    cycles (int):
        Info:
            Give the time until execution in cycles, this option is not recommended
            as it will change depending on framerate.
        Default:
            0

    seconds (float):
        Info:
            The time until execution in seconds, this option will overwrite cycles.
        Default:
            0

    timed (bool):
        Info:
            Whether or not the execution is timed (used with anykey.)
        Default:
            True

    anykey (bool):
        Info:
            If enabled, the given function will be executed when a KEYDOWN event
            is caught by eventHandler. Often used with timed=False.
        Default:
            True
    """
    def __init__(self, game, function, cycles=0, seconds=0.0, timed=True, anykey=True):
        super(TimedExecution, self).__init__(game, 0, 0)

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
            self.cycles = int(round(seconds * TETRIS_FRAMERATE))

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

class Tetromino(Job):
    """
    A tetromino, heavily tied in with the Board class, requires a board to function.

    Positional arguments:

    board (Board instance):
        The board that the instance belongs to 
    matrix (2d list):
        An image of the tetromino, given as a 2d matrix of boolean values
        Example:
            ## The "T" block
            [[0, 1, 0],
             [1, 1, 1]]
    _type (str):
        **DEPRECATED**
        The name of the tetromino, not actually used for anything but it was put in here in case
        it would be useful at some point.
    color (tuple):
        The color of the tetromino blocks given as a RGB tuple.
    """
    def __init__(self, board, matrix, _type, color, x=0, y=None, ycenter=False,
                 xcenter=False, ghostpiece=True, updateinterval=TETRIS_FRAMERATE, queue=None,
                 fill=False, keymap=None
                 ):

        assert matrix, "Will not create tetromino with empty matrix"

        super(Tetromino, self).__init__(board.game, x, y)

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
        self.move_right_timeout = None
        self.move_left_timeout = None
        self.force_draw = True
        self.keymap = keymap or Shared.keymap["game"]["player1"]

        if xcenter:
            self.x = (self.board.blocks_width//2) - (len(self.matrix[0])//2)

        if y == None:
            self.y = -(len(self.matrix))
        if ycenter:
            self.y = (self.board.blocks_height//2) - (len(self.matrix)//2)

        self.ghostpiece = None
        if ghostpiece:
            self.ghostpiece = GhostTetromino(
                board, matrix, _type,
                Shared.options["graphics"].get("ghostpiece_color", GHOST_COLOR), x=x, y=y, xcenter=xcenter
            )
            self.ghostpiece.drop(self.y)

        def speedUpKeyUpHandler():
            self.sped_up = False
            self.updateinterval = self.normal_speed
            self.time_until_update = self.updateinterval

        self.keyuphandlers = {
                self.keymap["speed_up"]   : lambda _: self.sped_up and speedUpKeyUpHandler(),
                self.keymap["move_right"] : lambda _: setattr(self, "move_right_timeout", None),
                self.keymap["move_left"]  : lambda _: setattr(self, "move_left_timeout", None),
                }

        def moveRightKeyDownHandler():
            self.moveHorizontal(1)
            self.move_right_timeout = Shared.options.get("move_tetromino_timeout", MOVE_TETROMINO_TIMEOUT) * TETRIS_FRAMERATE

        def moveLeftKeyUpHandler():
            self.moveHorizontal(-1)
            self.move_left_timeout = Shared.options.get("move_tetromino_timeout", MOVE_TETROMINO_TIMEOUT) * TETRIS_FRAMERATE

        def speedUpKeyDownHandler():
            self.sped_up = True
            self.normal_speed = self.updateinterval
            self.updateinterval = SPED_UP_UPDATEINTERVAL
            self.time_until_update = self.updateinterval

        self.keydownhandlers = {
                self.keymap["rotate_right"] : lambda _: self.rotate(1),
                self.keymap["rotate_left"]  : lambda _: self.rotate(-1),
                self.keymap["reverse"]      : lambda _: Shared.options["gameplay"].get("flip_tetromino") and self.flip(),
                self.keymap["move_right"]   : lambda _: moveRightKeyDownHandler(),
                self.keymap["move_left"]    : lambda _: moveLeftKeyUpHandler(),
                self.keymap["drop_down"]    : lambda _: self.drop(),
                self.keymap["speed_up"]     : lambda _: speedUpKeyDownHandler(),
                }

    def getActiveBlocks(self, x=None, y=None):
        for by in xrange(len(self.matrix)):
            for bx in xrange(len(self.matrix[by])):
                if self.matrix[by][bx]:
                    yield (x or self.x) + bx, (y or self.y) + by

    def getBlocksDict(self):
        blocks = {}
        for block in self.getActiveBlocks():
            blocks[block] = self.color
        return blocks

    def draw(self):
        if self.force_draw:
            if self.ghostpiece:
                self.ghostpiece.force_draw = True
                self.ghostpiece.draw()
            for x, y in self.getActiveBlocks():
                self.board.drawCube(x, y, self.color)
            self.board.layers.tetromino = self.getBlocksDict()
            self.board.emptyBlocks()
            self.force_draw = False

    def insert(self):
        self.board.layers.tetromino = {}

        if self.y < 0:
            ## XXX: GAME OVER
            self.board.update_required = False

        self.board.blocks.update(self.getBlocksDict())
        self.board.checkTetris()
        self.update_required = False
        self.ghostpiece.update_required = False

    def update(self):
        self.time_until_update -= 1
        if self.time_until_update <= 0:
            self.moveDiagonal(1)
            self.time_until_update = self.updateinterval

        if self.move_right_timeout != None:
            self.move_right_timeout -= 1
        if self.move_left_timeout != None:
            self.move_left_timeout -= 1

        if self.move_right_timeout != None and self.move_right_timeout <= 0:
            self.move_right_timeout = Shared.options.get("moving_tetromino_timeout", MOVING_TETROMINO_TIMEOUT) * TETRIS_FRAMERATE
            self.moveHorizontal(1)
        if self.move_left_timeout != None and self.move_left_timeout <= 0:
            self.move_left_timeout = Shared.options.get("moving_tetromino_timeout", MOVING_TETROMINO_TIMEOUT) * TETRIS_FRAMERATE
            self.moveHorizontal(-1)

    def drop(self):
        ## We now need to make sure that the update never happens by setting time_until_update to infinity,
        ## this fixes a bug where the block will occasionally be inserted twice (boohyeah)
        self.time_until_update = float('inf')
        while self.update_required:
            self.moveDiagonal(1)
        self.force_draw = True

    def checkBlockCollision(self, x=None, y=None):
        return any(self.board.blocks.get((x_, y_)) for x_, y_ in self.getActiveBlocks(x=x, y=y))

    def checkWallCollision(self, xp, yp):
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                ## Some of the functions need to know which edge the collision happened on,
                ## otherwise the result can be treated like a boolean.
                if self.matrix[y][x]:
                    if yp+y > self.board.blocks_height-1:
                        return "bottom"
                    if xp+x > self.board.blocks_width-1:
                        return "right"
                    if xp+x < 0:
                        return "left"

    ## Move diagonally, if possible
    def moveDiagonal(self, direction):
        self.y += direction
        self.force_draw = True
        if self.checkBlockCollision() or self.checkWallCollision(self.x, self.y) == "bottom":
            self.y -= direction
            self.insert()

    ## Move horizontally, if possible
    def moveHorizontal(self, direction):
        self.updateGhost("moveHorizontal", direction)
        self.force_draw = True
        self.x += direction
        if self.checkBlockCollision():
            self.x -= direction
        if self.checkWallCollision(self.x, self.y):
            self.x -= direction

    ## Rotate if possible
    def rotate(self, direction):
        last_matrix = self.matrix
        self.matrix = Matrix.rot90(self.matrix)
        self.force_draw = True

        positions = []
        for y in xrange(-MAX_VERTICAL_AUTO_MOVE, MAX_VERTICAL_AUTO_MOVE+1):
            positions.append(
                    [(self.x + x, self.y + y) for x in xrange(-MAX_HORIZONTAL_AUTO_MOVE, MAX_HORIZONTAL_AUTO_MOVE+1)]
                    )

        def digOutward(condition, xs):
            pass

        def macroGoodPos(xss):
            def microGoodPos(xs):
                def atomGoodPos(x, y):
                    is_good = not (self.checkWallCollision(x, y) or self.checkBlockCollision(x=x, y=y))
                    if is_good:
                        return x, y
                    return None
                jump = 0
                middle = int(round(len(xs) / 2.0)) - 1
                while True:
                    ## TODO: Make this procedure into a function
                    position = atomGoodPos(*xs[ middle + jump ]) or atomGoodPos(*xs[ middle - jump ])
                    if position:
                        return position
                    jump += 1
                    if middle - jump < 0 and middle + jump >= len(xs):
                        return None
            jump = 0
            middle = int(round(len(xss) / 2.0)) - 1
            while True:
                ## TODO: Make this procedure into a function
                position = ( contain(lambda: microGoodPos(xss[ middle - jump ]), (IndexError,)) or
                             contain(lambda: microGoodPos(xss[ middle + jump ]), (IndexError,)) )
                if position:
                    return position
                jump += 1
                if middle - jump < 0 and middle + jump >= len(xss):
                    return None

        position = macroGoodPos(positions)
        if position:
            self.x, self.y = position
            self.updateGhost("rotate", direction)
        else:
            self.matrix = last_matrix

    def updateGhost(self, attr, *args, **kwargs):
        if self.ghostpiece:
            self.ghostpiece.force_draw = True
            self.ghostpiece.y = self.y
            self.ghostpiece.x = self.x
            getattr(self.ghostpiece, attr)(*args, **kwargs)
            self.ghostpiece.drop(self.y)

    ## It makes the game WAAY to easy, but i kind of always wondered "what if"
    def flip(self):
        self.force_draw = True
        if not (self.checkWallCollision(self.x, self.y) or self.checkBlockCollision()):
            Matrix.flip(self.matrix)
            self.updateGhost("flip")

class GhostTetromino(Tetromino):
    """
    "GhostPiece"
    Should always be managed by a Tetromino, should not be registered as a Job.
    """
    def __init__(self, *args, **kwargs):
        super(GhostTetromino, self).__init__(*args, ghostpiece=False, **kwargs)

    def insert(self):
        raise TypeError("Attempted to insert Ghost")

    def drop(self, y_pos):
        for y in xrange(y_pos, self.board.height):
            self.y = y
            if self.checkBlockCollision() or self.checkWallCollision(self.x, self.y) == "bottom":
                ## We need to be one step away from the next collision
                self.y -= 1
                break

    def draw(self):
        if self.force_draw:
            for x, y in self.getActiveBlocks():
                self.board.drawCube(x, y, self.color, shade=False)
            self.board.layers.ghost_tetromino = self.getBlocksDict()
            self.force_draw = False

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
        if kwargs.get("x"):
            self.x = kwargs["x"]
        if kwargs.get("y"):
            self.y = kwargs["y"]

    def update(self):
        super(ScrollingText, self).update()

        if (self.y >= self.game.height and self.speed > 0) or (self.y + self.height <= 0 and self.speed < 0):
            self.update_required = False
            return

        self.y += self.speed

class Notification(TextBox):
    """
    Notification that will destroy itself when clicked.
    """
    def __init__(self, game, _id, text):
        super(Notification, self).__init__(
                game, text, xcenter=True, ycenter=True, font=ERRORBOX_FONT,
                textfit=True, onmouseclick=lambda: game.removeJob(_id),
                colors=ERRORBOX_COLORSCHEME, background=True, border=True,
                padding=6,
                )

class Board(Job):
    def __init__(self, game, x=0, y=0, blockwidth=0, width=0, height=0, bgcolor=(0x3f,0x3f,0x3f), draw_border=True,
                 innercolor=(0x3F,0x3F,0x3F), outercolor=(0x50,0x50,0x50), queue=Queue.BOARD, level=1, draw_grid=True,
                ):
        super(Board, self).__init__(game, x, y)

        self.anchor = (x, y)
        self.draw_border = draw_border
        self.x = x
        self.y = y
        self.blocks_width = width
        self.blocks_height = height
        self.width = width * blockwidth
        self.height = height * blockwidth
        self.blocks = {}
        self.layers = Struct()
        self.layers.tetromino = {}
        self.layers.ghost_tetromino = {}
        self.drawncubes = set()
        self.blockwidth = blockwidth
        self.game = game
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
        ##      are given in BOARD_BLOCKWIDTH, not pixels.
        self.fill = False

    def drawCube(self, x, y, color, shade=None):
        if shade == None:
            shade = Shared.options["graphics"].get("shade")

        if y < 0 or x < 0 or x >= self.blocks_width or y >= self.blocks_height:
            ## Out of bounds
            return

        self.drawncubes.add((x, y))

        Pygame.draw.rect(
            self.game.screen,
            color,
            (self.x + x*self.blockwidth + 1, self.y + y*self.blockwidth + 1, self.blockwidth - 1, self.blockwidth - 1)
        )

        ## Draw shade
        if shade:
            ## Top shade (actually light, but whatever)
            x, y = self.x + x*self.blockwidth + 1, self.y + y*self.blockwidth + 1
            Pygame.draw.polygon(
                    self.game.screen,
                    RGB.dial(color, 50),
                    ((x, y+1), (x + self.blockwidth - 2, y+1),
                     (x + 2, y + 2), (x + self.blockwidth - 3, y + 2)),
                    0,
                    )
            ## Bottom shade
            Pygame.draw.polygon(
                    self.game.screen,
                    RGB.dial(color, -50),
                    ((x, y+self.blockwidth - 2), (x + self.blockwidth - 2, y+self.blockwidth - 2),
                     (x + 4, y + self.blockwidth - 3), (x + self.blockwidth - 5, y + self.blockwidth - 3)),
                    0,
                    )

            if Shared.options["graphics"].get("cross_tetromino"):
                ## Draw cool "cross" shade
                Pygame.draw.polygon(
                        self.game.screen,
                        RGB.dial(color, -30),
                        ((x, y+1), (x, y+self.blockwidth - 3),
                         (x + 4, y + self.blockwidth - 3), (x + self.blockwidth - 5, y + self.blockwidth - 3)),
                        0,
                        )
            else:
                ## Draw other shades
                Pygame.draw.polygon(
                        self.game.screen,
                        RGB.dial(color, -30),
                        ((x, y+1), (x, y+self.blockwidth - 3),
                         (x + 4, y + self.blockwidth - 3), (x + 4, y + self.blockwidth - 3)),
                        0,
                        )

    def getRows(self):
        rows = self.blocks_height
        # for row in xrange(rows):
        #     yield [(x, y) in self.blocks for x, y in self.blocks if y == row]
        for row in xrange(rows):
            yield [(x, row) in self.blocks for x in xrange(self.blocks_width)]

    def checkTetris(self, rows=None):
        if rows == None:
            rows = xrange(self.blocks_height)

        lines = 0

        for row in rows:
            points = [p for p in self.blocks if p[1] == row]
            if len(points) == self.blocks_width:
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
            ## Empty all cubes
            for x, y in set(self.drawncubes):
                Pygame.draw.rect(
                    self.game.screen,
                    self.bgcolor,
                    (self.x + x*self.blockwidth + 1, self.y + y*self.blockwidth + 1, self.blockwidth - 1, self.blockwidth - 1)
                )
                self.drawncubes.discard((x, y))

            ## Force a redraw
            self.force_draw = True
            self.score += TETRIS_SCORES.get(lines, TETRIS_SCORES_OTHER)

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
            self.drawAllBlocks()

        self.isupdated = False
        self.force_draw = False

    def emptyBlocks(self):
        active_blocks = set()
        active_blocks.update(self.blocks)
        for blocks in self.layers.__dict__:
            active_blocks.update(getattr(self.layers, blocks))
        blocks = self.drawncubes.difference(active_blocks)
        for x, y in blocks:
            Pygame.draw.rect(
                self.game.screen,
                self.bgcolor,
                (self.x + x*self.blockwidth + 1, self.y + y*self.blockwidth + 1, self.blockwidth - 1, self.blockwidth - 1)
            )
            self.drawncubes.discard((x, y))

    ## TODO: Instead of having the Tetromino call Board.drawBlock, this could instead be handled by
    ##       this (drawNewBlocks) function.
    def drawNewBlocks(self):
        for block in self.drawncubes.difference(self.blocks):
            if self.blocks.get(block):
                self.drawCube(block[0], block[1], self.blocks[block])

    def drawAllBlocks(self):
        for x, y in self.blocks:
            self.drawCube(x, y, self.blocks[(x, y)])

    def drawBoard(self):
        """ Yup, just draw the board """

        if self.draw_border:
            Pygame.draw.rect(
                    self.game.screen,
                    self.outercolor,
                    (self.x, self.y, (self.blocks_width * self.blockwidth) + 1, self.blocks_height * self.blockwidth + 1),
                    1)
        Pygame.draw.rect(
                self.game.screen,
                self.bgcolor,
                (self.x+1, self.y+1, self.blocks_width * self.blockwidth - 2, self.blocks_height * self.blockwidth - 1),
                0)
        if self.draw_grid:
            for x in xrange(1, self.blocks_width):
                Pygame.draw.line(
                        self.game.screen,
                        self.innercolor,
                        (self.x + self.blockwidth*x, self.y + 1),
                        (self.x + self.blockwidth*x, self.y + self.blocks_height*self.blockwidth - 2),
                        1)
            for y in xrange(1, self.blocks_height):
                Pygame.draw.line(
                        self.game.screen,
                        self.innercolor,
                        (self.x + 1, self.y + self.blockwidth*y),
                        (self.x + self.blocks_width*self.blockwidth - 2, self.y + self.blockwidth*y),
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

class Filler(Job):
    def __init__(self, game, x, y, width, height, color=None, queue=Queue.GENERIC):
        super(Filler, self).__init__(game, x, y)
        self.color = color or self.game.bgcolor
        self.queue = queue
        self.width = width
        self.height = height

    def draw(self):
        Pygame.draw.rect(
                self.game.screen,
                self.color,
                (self.x, self.y, self.width, self.height),
                )

class Table(Job):
    def __init__(self, game, x, y, font, table, xcenter=False, ycenter=False, header_font=None, colors={}, onmouseclick=(lambda seq, columns: None),
                 border_width=1, **kwargs):
        super(Table, self).__init__(game, x, y, **kwargs)

        self.rows = [columns for columns, _ in table]
        self.colors = copy(colors)
        self.font = font
        self.spacer = 2
        self.onmouseclick = onmouseclick
        self.table = table
        self.xcenter = xcenter
        self.ycenter = ycenter
        self.border_width = border_width

        if not header_font:
            header_font = font

        self.renderFonts()

    def renderFonts(self):
        font = loadFont(self.font)

        ## Simplest method of padding, let the font renderer handle it automatically by adding spaces.
        rows = [ [u" {} ".format(column) for column in row]
                 for row in self.rows ]

        self.column_widths = [0 for _ in xrange(len(rows[0]))]
        self.row_heights = []
        self.rendered_rows = []
        for row in rows:
            columns = []
            for i in xrange(len(row)):
                width, height = font.size(row[i])
                if self.column_widths[i] < width:
                    self.column_widths[i] = width
                columns.append(font.render(row[i], True, self.colors["font"]))
            self.row_heights.append(height)
            self.rendered_rows.append(columns)
        self.width = sum(self.column_widths)
        self.height = sum(self.row_heights)

        if self.xcenter:
            self.x = (self.game.width // 2) - (self.width // 2)
        if self.ycenter:
            self.y = (self.game.height // 2) - (self.height // 2)

    def draw(self):
        ## Fill the area
        Pygame.draw.rect( self.game.screen, self.colors["background"], (self.x, self.y, self.width, self.height), 0)

        ## Draw fonts
        y = self.y
        for row_i in xrange(len(self.rendered_rows)):
            row = self.rendered_rows[row_i]
            x = self.x
            for column_i in xrange(len(row)):
                column = row[column_i]
                self.game.screen.blit(column, (x, y))
                x += self.column_widths[column_i]
            y += self.row_heights[row_i]

        ## Draw borders between rows
        y = self.y
        for row_i in xrange(len(self.rendered_rows)):
            Pygame.draw.line(self.game.screen, self.colors["border"], (self.x, y), (self.x + self.width, y), self.border_width)
            y += self.rendered_rows[row_i][0].get_height()

        ## Draw borders between columns
        x = self.x
        for column_i in xrange(len(self.rendered_rows[0])):
            Pygame.draw.line(self.game.screen, self.colors["border"], (x, self.y), (x, self.y + self.height), self.border_width)
            x += self.column_widths[column_i]

        ## Draw a box around everything
        Pygame.draw.rect( self.game.screen, self.colors["border"], (self.x, self.y, self.width + 1, self.height + 1), self.border_width)

    def eventHandler(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button in (1, 3):
                x, y = Pygame.mouse.get_pos()
                row = (y - self.y) / self.row_heights[0]
                if (0 <= row <= len(self.rows)-1) and (self.x <= x <= self.x + self.width):
                    self.onmouseclick(row, self.table[row][0], self.table[row][1])

class InputBox(TextBox):
    def __init__(self, game, prompt, maxlen=20, submit_key=Pygame.K_RETURN, colors=ERRORBOX_COLORSCHEME, font=ERRORBOX_FONT, noncharacters=NONCHARACTERS,
                 required_length=1, require_nonwhitespace=True):
        text = unicode(prompt + "{input}")
        self.maxlen = maxlen
        self.value = u""
        self.submit_key = submit_key
        self.noncharacters = tuple(noncharacters) + (submit_key,)
        self.required_length = required_length
        self.require_nonwhitespace = require_nonwhitespace
        Pygame.key.set_repeat(KEYDOWN_REPEAT_DELAY, KEYDOWN_REPEAT_INTERVAL)
        super(InputBox, self).__init__(
                game, text, xcenter=True, ycenter=True, font=font,
                textfit=True, colors=colors, background=True, border=True,
                padding=12, variables={"input": lambda _: self.value}, border_width=2,
                )

    def eventHandler(self, event):
        if event.type == KEYDOWN:
            if event.key == self.submit_key:
                if len(self.value) < self.required_length:
                    return
                if self.require_nonwhitespace and all(c.isspace() for c in self.value):
                    return
                Log.debug(u"Submitting {} from `{}'".format(repr(self.value), self))
                self.update_required = False
                Pygame.key.set_repeat()

            if event.key == K_BACKSPACE:
                self.value = self.value[:-1]
                self.resize = True
                Pygame.draw.rect(
                        self.game.screen,
                        self.game.bgcolor,
                        (self.x-self.border_width, self.y-self.border_width, self.width+self.border_width + 1, self.height+self.border_width + 1)
                        )
            else:
                if event.key in self.noncharacters:
                    return
                if len(self.value) >= self.maxlen:
                    return
                try:
                    mods = Pygame.key.get_mods()
                    if mods & KMOD_SHIFT or mods & KMOD_CAPS:
                        self.value += unichr(event.key).upper()
                    else:
                        self.value += unichr(event.key)
                except UnicodeEncodeError:
                    return
            self.game.lock[KEYDOWN] = self

class Border3D(Job):
    """
    3d border with background, draws four polygons (creating the 3d effect)
    and one rectangle (filling the background)
    """
    def __init__(self, game, x, y, width, height, colors, deepness, background=None, **kwargs):
        super(Border3D, self).__init__(game, x, y, **kwargs)
        self.force_draw = True
        self.width = width
        self.height = height
        self.colors = colors
        self.deepness = deepness
        self.background = background

    def draw(self):
        if self.force_draw:
            Draw.draw3DBorder(
                    self.game.screen,
                    self.colors,
                    (self.x, self.y, self.width, self.height),
                    self.deepness,
                    background=self.background
                    )
            self.force_draw = False

