#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Core classes that are derived from
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

## Classes that are never used directly, only derived from

import pygame as Pygame
import sys as Sys
import Log
import Shared
from pygame.locals import *
from Globals import *
from Jobs import TextBox

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
        self.lock = {}

        self.setup()

    def removeJob(self, job):
        delattr(self.jobs, job)

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
        Log.log("Exiting from `{}'".format(self))
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
        Log.log("Returning from Game `{}'".format(self))

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

    def eventHandler(self, event):
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
                    for event in self.events:
                        if event.type not in self.lock:
                            obj.eventHandler(event)
                if obj.draw_required:
                    obj.draw()


            Pygame.display.flip()

            for event in self.events:
                if event.type not in self.lock:
                    self.eventHandler(event)

            if self.running:
                self.running()

            ## Remove locks
            self.lock = {}

        return self.ret

## TODO: Add sliders and other fancy shit
class Menu(Game):
    def __init__(self, _id, header_font={"size":60, "bold":False}, option_font={"size":60, "bold":False}, decorate_options=False, isroot=False, **kwargs):
        self.id = _id
        super(Menu, self).__init__(self.id, **kwargs)
        self.running = self.mainLoop
        self.colorscheme = MENU_COLORSCHEME
        self.header = ""
        self.menu = []
        self.lookup = {}
        self.options = []
        self.selected = 0
        self.options_pos = (10, 80)
        self.header_font = header_font
        self.option_font = option_font
        self.isroot = isroot

    def setupObjects(self):
        def mouseLeave(box):
            box.colors["font"] = self.colorscheme["option"]
        def mouseEnter(box):
            box.colors["font"] = self.colorscheme["selected"]

        if not self.isroot and self.menu[-1][0] != "Back":
            self.menu.append(("Back", self.quitGame))

        self.addJob("header",
                TextBox(self, self.header, y=20, xcenter=True, textfit=True, underline=False,
                        colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)}, font=self.header_font,
                        )
                )
        self.lookup = dict(self.menu)
        x, y = self.options_pos
        self.options = []
        for option, func in self.menu:
            Log.debug("Creating TextBox with {} at {}".format(repr(option), (x, y)))
            self.options.append("{}".format(option))
            self.addJob("{}".format(option),
                    TextBox(self, option, y=y, x=x, textfit=True,
                        colors={
                            "background":self.colorscheme["background"],
                            "font":self.colorscheme["option"],
                            },
                        font=self.option_font,
                        onmouseclick=func,
                        onmouseenter=mouseEnter,
                        onmouseleave=mouseLeave,
                        )
                    )
            y += self.getJob("{}".format(option)).fontheight

    def mainLoop(self):
        pass

    def move(self, direction):
        item = self.getSelectedItem()
        obj = self.getJob(self.menu[item][0])
        if item == len(self.menu)-1 and direction == 1:
            newobj = self.getJob(self.menu[0][0])
        elif item == 0 and direction == -1:
            newobj = self.getJob(self.menu[len(self.menu)-1][0])
        else:
            newobj = self.getJob(self.menu[item+direction][0])
        obj.onmouseleave(obj)
        obj.hasmouse = False
        newobj.onmouseenter(newobj)
        newobj.hasmouse = True
        Log.log("Moving cursor to {}".format(repr(newobj.text)))

    def getSelectedItem(self):
        for i in xrange(len(self.menu)):
            option, func = self.menu[i]
            if self.getJob(option).hasmouse:
                break
        else:
            return 0
        return i

    def changeMenu(self, menu):
        self.call(menu)

    def close(self):
        self.quitGame()

    def execOption(self):
        ## Right now each option just runs a function, this may change
        option = self.lookup[self.options[self.getSelectedItem()]]
        option()

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

        if event.type == KEYDOWN:
            if event.key == Shared.keymap["menu"]["back"]:
                self.close()
            elif event.key == Shared.keymap["menu"]["down"]:
                self.move(1)
            elif event.key == Shared.keymap["menu"]["up"]:
                self.move(-1)
            elif event.key == Shared.keymap["menu"]["select"]:
                self.execOption()

## TODO: Add sliders and other fancy shit
class NMenu(Game):
    def __init__(self, _id, header_font={"size":60, "bold":False}, option_font={"size":60, "bold":False}, decorate_options=False,
                 isroot=False, onHeaderClick=None, **kwargs):
        self.id = _id
        super(NMenu, self).__init__(self.id, **kwargs)
        self.running = self.mainLoop
        self.colorscheme = MENU_COLORSCHEME
        self.header = ""
        self.menu = []
        self.lookup = {}
        self.options = []
        self.selected = 0
        self.options_pos = (10, 80)
        self.header_font = header_font
        self.option_font = option_font
        self.isroot = isroot
        self.onHeaderClick = onHeaderClick

    def setupObjects(self):
        def mouseLeave(box):
            Log.debug(box)
            box.colors["font"] = self.colorscheme["option"]
        def mouseEnter(box):
            Log.debug(box)
            box.colors["font"] = self.colorscheme["selected"]

        if not self.isroot and self.menu[-1][0] != "Back":
            self.menu.append(("Back", self.quitGame))

        self.addJob("header",
                TextBox(self, self.header, y=20, xcenter=True, textfit=True, underline=False,
                        colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)}, font=self.header_font,
                        onmouseclick=self.onHeaderClick
                        )
                )
        self.lookup = dict([(option.text, option) for option in self.menu])
        x, y = self.options_pos
        self.options = []
        ## Set options, then add the job
        for option in self.menu:
            option.x = x
            option.y = y
            option.onmouseleave = mouseLeave
            option.onmouseenter = mouseEnter
            self.addJob(option.text, option)
            self.options.append(option.text)
            y += option.height

    def mainLoop(self):
        pass

    def move(self, direction):
        item = self.getSelectedItem()
        obj = self.getJob(self.menu[item][0])
        if item == len(self.menu)-1 and direction == 1:
            newobj = self.getJob(self.menu[0][0])
        elif item == 0 and direction == -1:
            newobj = self.getJob(self.menu[len(self.menu)-1][0])
        else:
            newobj = self.getJob(self.menu[item+direction][0])
        obj.onmouseleave(obj)
        obj.hasmouse = False
        newobj.onmouseenter(newobj)
        newobj.hasmouse = True
        Log.log("Moving cursor to {}".format(repr(newobj.text)))

    def getSelectedItem(self):
        for i in xrange(len(self.menu)):
            option, func = self.menu[i]
            if self.getJob(option).hasmouse:
                break
        else:
            return 0
        return i

    def changeMenu(self, menu):
        self.call(menu)

    def close(self):
        self.quitGame()

    def execOption(self):
        ## Right now each option just runs a function, this may change
        option = self.lookup[self.options[self.getSelectedItem()]]
        option()

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

        if event.type == KEYDOWN:
            if event.key == Shared.keymap["menu"]["back"]:
                self.close()
            elif event.key == Shared.keymap["menu"]["down"]:
                self.move(1)
            elif event.key == Shared.keymap["menu"]["up"]:
                self.move(-1)
            elif event.key == Shared.keymap["menu"]["select"]:
                self.execOption()

