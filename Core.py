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
import Jobs
from PythonShouldHaveTheseThingsByDefaultTheyAreJustTooFuckingHelpful import *

class Game(object):
    def __init__(self, _id, caption="", mouse_visible=True, bgcolor=(0x22,0x22,0x22), screen=None, ticktime=FRAMERATE,
                 width=SCREEN_WIDTH, height=SCREEN_HEIGHT, x=SCREEN_WIDTH, y=SCREEN_HEIGHT, sound_enabled=False, soundtrack=None,
                 fill=True):
        Log.debug("Initializing Game object `{}'".format(_id))
        self.jobs = Struct()
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
        self.fill = fill

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
        except Pygame.error:
            Log.error("Unable to play music file: `{}'".format(path))

    def getJob(self, name):
        return getattr(self.jobs, name)

    def addJob(self, name, obj):
        setattr(self.jobs, name, obj)

    ## Why not just call Sys.exit(), why create a separate method for this?
    ## Because finishing off can get more complex as this program develops.
    def quit(self):
        Log.debug("Exiting from `{}'".format(self))
        Sys.exit()

    ## We just "exploit" the stack to create things like pause menus or other "contexts"
    ## that take over the screen.
    def call(self, obj, *args, **kwargs):
        game = obj(screen=self.screen, *args, **kwargs)
        ret = game.run()

        self.setup()

        for job in self.jobs.__dict__:
            self.jobs.__dict__[job].force_draw = True

        if ret and self.id != ret:
            self.quitGame(ret)

    def quitGame(self, *args):
        if args:
            self.ret = args[0]
        if self.playing:
            self.stopMusic()
        self.running = None
        Log.debug("Returning from Game `{}'".format(self))

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
                    if obj.fill:
                        Pygame.draw.rect(
                                self.screen,
                                self.bgcolor,
                                (obj.x, obj.y, obj.width, obj.height)
                                )
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
    def __init__(self, _id, header_font={"size":60, "bold":False}, option_font={"size":60, "bold":False}, decorate_options=False,
                 isroot=False, onHeaderClick=None, xcenter=False, **kwargs):
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
        self.onHeaderClick = onHeaderClick
        self.xcenter = xcenter

    def setupObjects(self):
        def mouseLeave(box):
            Log.debug(box)
            box.colors["font"] = self.colorscheme["option"]
        def mouseEnter(box):
            Log.debug(box)
            box.colors["font"] = self.colorscheme["selected"]

        if not self.isroot and self.menu[-1].text != "Back":
            self.menu.append(Jobs.AutoTextBox(self, "Back", onmouseclick=self.quitGame,
                                              font=MENU_OPTION_FONT,
                                              colors={
                                                  "background":self.colorscheme["background"],
                                                  "font":self.colorscheme["option"],
                                                  }
                                              ))

        self.addJob("header",
                Jobs.TextBox(self, self.header, y=20, xcenter=True, textfit=True, underline=False,
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
            if self.xcenter:
                option.x = (self.width // 2) - (option.width // 2)
            option.y = y
            if option.text == "Back":
                option.y = y + SPACER
            option.onmouseleave = mouseLeave
            option.onmouseenter = mouseEnter
            self.addJob(option.text, option)
            self.options.append(option.text)
            y += option.height

    def mainLoop(self):
        pass

    def move(self, direction):
        item = self.getSelectedItem()
        obj = self.menu[item]
        if item == len(self.menu)-1 and direction == 1:
            newobj = self.menu[0]
        elif item == 0 and direction == -1:
            newobj = self.menu[len(self.menu)-1]
        else:
            newobj = self.menu[item+direction]
        obj.onmouseleave(obj)
        obj.hasmouse = False
        newobj.onmouseenter(newobj)
        newobj.hasmouse = True
        Log.debug("Moving cursor to {}".format(repr(newobj.text)))

    def getSelectedItem(self):
        for i in xrange(len(self.menu)):
            option = self.menu[i].text
            func = self.menu[i].onmouseclick
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
        option.onmouseclick()

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

