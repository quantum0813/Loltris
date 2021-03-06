#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Core functionality of the game, multi-purpose classes that are derived
## from elsewhere (and here)
## 
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

## Classes that are never used directly, only derived from

import pygame as Pygame
import sys as Sys
import Log
import Load
import Shared
from pygame.locals import *
from Globals import *
import Jobs
import JobQueue
import Draw
import threading as Threading
from DataTypes import *

class GameError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Game(object):
    """
    Multi-purpose class for creating and managing games. Based on the handling of multiple jobs in a perticular
    order, can be thought of as a (very) minimal operating system for video games.
    """
    def __init__(self, _id, caption="", mouse_visible=True, bgcolor=(0x22,0x22,0x22), screen=None, ticktime=TETRIS_FRAMERATE,
                 width=SCREEN_WIDTH, height=SCREEN_HEIGHT, x=SCREEN_WIDTH, y=SCREEN_HEIGHT, sound_enabled=True, soundtrack=None,
                 fill=True, icon=WM_ICON):
        Log.debug("Initializing Game object `{}'".format(_id))
        self.jobs = Struct()
        self.caption = caption
        self.mouse_visible = mouse_visible
        self.bgcolor = bgcolor
        self.screen = screen
        self.ticktime = ticktime
        self.ret = 0
        self.windows = {}
        self.height = height
        self.width = width
        self.events = None
        self.id = _id
        self.soundtrack = soundtrack
        self.sound_enabled = sound_enabled
        self.playing = ""
        self.lock = {}
        self.fill = fill
        self.threads = Struct()
        self.running = self.mainLoop

        ## TODO: Explore this
        self.interrupt_table = Struct(
            halt = self.quit
        )
        self.interrupts = []

    def mainLoop(self):
        pass

    def registerInterrupt(self, name, func):
        setattr(self.interrupt_table, name, func)

    def unregisterInterrupt(self, name):
        delattr(self.interrupt_table, name)

    def addThread(self, name, function, args=()):
        Log.notice("Launching thread {!r} for {!r}".format(name, self.id))
        self.threads[name] = Threading.Thread(target=function, args=args)
        self.threads[name].daemon = True
        self.threads[name].start()

    def removeJob(self, removed_job_str):
        removed_job = getattr(self.jobs, removed_job_str)
        ## For now this is the solution, fill the entire screen. When the todo below is finished,
        ## I'll just fill  the job instead.
        Draw.fillJob(self.screen, self.bgcolor, removed_job)
        for job in self.getJobsIn(removed_job_str):
            job.force_draw = True
        delattr(self.jobs, removed_job_str)

    def stopMusic(self):
        if self.playing:
            self.playing = ""
            Pygame.mixer.music.stop()
        else:
            Log.warning("Attempted to stop music while no music was playing in `{}'".format(self.id))

    ## TODO: The call/quit model currently fails here, I'll just have to save the music's "progress."
    def playMusic(self, path, loops=1, pos=0.0):
        try:
            if not self.sound_enabled:
                ## Should never happen
                Log.panic("Attempted to play music in `{}' where sound has been disabled".format(self.id))
            Pygame.mixer.music.load(path)
            Pygame.mixer.music.play(loops, pos)
            self.playing = path
            Log.debug("Playing sountrack `{}'".format(path))
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
        
        Log.debug("Calling `{}' from `{}'".format(game.id, self.id))

        if Pygame.mixer.music.get_busy():
            music_pos = Pygame.mixer.music.get_pos()

        if self.playing and not game.sound_enabled:
            Log.debug("Stopping soundtrack `{}' at {}".format(self.playing, Pygame.mixer.music.get_pos()))
            Pygame.mixer.music.pause()

        game.setup()
        ret = game.run()

        if ret and self.id != ret:
            self.quitGame(ret)

        ## TODO: Make the music start where it stopped, there appears to be an issue with Pygame.mixer
        ##       that makes this impossible. The game freezes when Pygame.mixer.set_pos is called.
        ## Restore music 
        if game.soundtrack and self.playing:
            Log.debug("Restarting music, was playing `{}'".format(self.playing))
            self.playMusic(self.playing, pos=music_pos)

        ## XXX: What if the game with no sound playing launches a game that plays sound?
        if self.playing and not game.sound_enabled:
            Pygame.mixer.music.unpause()

        self.setup()

        ## Force redrawing of all jobs (if they support it)
        for job in self.jobs:
            self.jobs.__dict__[job].force_draw = True


    def quitGame(self, *args):
        if args:
            self.ret = args[0]
        self.running = None
        for thread in self.threads:
            thread._Thread__stop()
        Log.debug("Returning from Game `{}'".format(self))

    def setup(self):
        Log.debug("Running setup for {}".format(self.id))

        Pygame.init()
        Pygame.mouse.set_visible(int(self.mouse_visible))
        Pygame.display.set_icon(Load.loadImage(WM_ICON))

        if not Pygame.mixer.get_init() and self.sound_enabled:
            Log.log("Initializing mixer")
            Pygame.mixer.init()

        if self.soundtrack and self.sound_enabled and not self.playing:
            Log.debug("Playing music: {}".format((self.soundtrack, self.sound_enabled, self.playing)))
            self.playMusic(self.soundtrack, loops=-1)

        if not self.screen or self.screen.get_width() != self.width or self.screen.get_height() != self.height:
            Log.notice("Setting display mode {}".format((self.width, self.height)))
            self.screen = Pygame.display.set_mode((self.width, self.height), DISPLAY_OPTIONS)


        self.screen.fill(self.bgcolor)
        Pygame.display.flip()
        self.clock = Pygame.time.Clock()
        Pygame.display.set_caption(self.caption)

    def eventHandler(self, event):
        pass

    def getJobsIn(self, basename):
        base = self.getJob(basename)
        for jobname in self.jobs:
            if jobname == basename:
                ## Skip the base itself
                continue

            job = self.getJob(jobname)

            if not job.draw_required:
                ## Does not draw anything to the screen
                continue

            if job.x <= base.x <= job.width + job.x and job.y <= base.y <= job.height + job.y:
                yield job


    def handleInterrupts(self):
        for interrupt in self.interrupts:
            if not hasattr(self.interrupt_table, interrupt):
                raise LookupError("Invalid interrupt {} not in table".format(interrupt))
            ## Run the handler
            getattr(self.interrupt_table, interrupt)()

    def run(self):
        if not hasattr(self, "running") or not hasattr(self, "eventHandler"):
            raise GameError("Game has not been properly initialized")

        timers = Struct(
                print_framerate = 0,
                )

        while self.running:

            for timer in timers:
                timers[timer] += 1

            self.clock.tick(self.ticktime)
            self.events = Pygame.event.get()
            self.interrupts = []

            if timers.print_framerate == TETRIS_FRAMERATE * DISPLAY_TETRIS_FRAMERATE_INTERVAL:
                timers.print_framerate = 0
                Log.notice("Framerate: {}".format(int(round(self.clock.get_fps()))))

            ## The events and updates should be handled in reverse order (the things on top go first)
            queue = sorted(self.jobs, key=lambda obj: getattr(self.jobs, obj).queue, reverse=True)
            for objname in queue:
                if objname not in self.jobs:
                    ## In case a Job modifies self.jobs, removing this job.
                    continue

                obj = self.getJob(objname)
                if obj.handling_events:
                    for event in self.events:
                        if event.type not in self.lock:
                            obj.eventHandler(event)

                ## XXX: This second check of update_required is necessarry because the eventHandler may either modify
                ##      or call methods that modify parameters in obj.
                if obj.update_required:
                    obj.update()

            queue = sorted(self.jobs, key=lambda obj: getattr(self.jobs, obj).queue)
            ## Handle resizing (redraw everything underneath the resized job)
            for objname in queue:
                obj = self.getJob(objname)
                if obj.__dict__.get("resize"):
                    for job in self.getJobsIn(objname):
                        job.force_draw = True
                    obj.resize = False

            ## Unlike the events and updates, drawing is handled so that the lowest go first
            for objname in queue:

                if objname not in self.jobs:
                    ## In case a Job modifies self.jobs, removing this job.
                    continue

                obj = self.getJob(objname)

                if objname not in self.jobs:
                    ## In case a Job modifies self.jobs, removing itself during update.
                    continue

                if obj.draw_required:
                    if obj.fill:
                        Draw.fillJob(self.screen, obj.fill, obj)
                    obj.draw()


            Pygame.display.flip()

            for event in self.events:
                if event.type not in self.lock:
                    self.eventHandler(event)

            if self.running:
                self.running()

            ## Remove locks
            self.lock = {}

            self.handleInterrupts()

        return self.ret

class Menu(Game):
    """
    Game-derived class for creating Menus.
    """
    def __init__(self, _id, header_font={"size":60, "bold":False}, option_font={"size":60, "bold":False}, decorate_options=False,
                 isroot=False, onHeaderClick=None, xcenter=False, **kwargs):
        self.id = _id
        super(Menu, self).__init__(self.id, ticktime=MENU_FRAMERATE, **kwargs)
        self.running = self.mainLoop
        self.colorscheme = MENU_COLORSCHEME
        self.header = ""
        self.menu = []
        self.lookup = {}
        self.options = []
        self.selected = 0
        self.options_pos = [10, 90] ## Needs to be mutable
        self.header_font = {}
        self.header_font.update(header_font)
        self.option_font = {}
        self.option_font.update(option_font)
        self.isroot = isroot
        self.onHeaderClick = onHeaderClick
        self.xcenter = xcenter
        self.added = Struct(
                back_button = None
                )

    def setupObjects(self):
        def mouseLeave(box):
            box.colors["font"] = self.colorscheme["option"]
            box.renderFonts()
        def mouseEnter(box):
            Log.debug(box)
            box.colors["font"] = self.colorscheme["selected"]
            box.renderFonts()

        if not self.isroot and not self.added.back_button:
            self.menu.append(Jobs.AutoTextBox(self, "Back", onmouseclick=self.quitGame,
                                              font=MENU_OPTION_FONT,
                                              colors={
                                                  "background":self.colorscheme["background"],
                                                  "font":self.colorscheme["option"],
                                                  },
                                              fill=MENU_3DBORDER_BACKGROUND,
                                              ))
            self.added.back_button = True

        if self.header:
            Log.debug("Adding header `{}' for `{}'".format(self.header, self.id))
            self.addJob("header",
                    Jobs.TextBox(self, self.header, y=20, xcenter=True, textfit=True, underline=False,
                            colors={"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa)}, font=self.header_font,
                            onmouseclick=self.onHeaderClick, queue=JobQueue.HEADER, fill=self.bgcolor,
                            )
                    )
        else:
            Log.warning("No header text given to Menu `{}'".format(self.id))

        self.addJob(
                "scroll_filler",
                Jobs.Filler(
                    self, 0, 0, self.width, self.options_pos[1] - SPACER,
                    queue=JobQueue.SCROLL_FILLER,
                    )
                )

        self.lookup = dict([(option.text, option) for option in self.menu])
        x, y = self.options_pos
        self.options = []

        options_height = sum(option.height for option in self.menu)
        if options_height + y > self.height:
            Log.warning("Height of all options combined exceeds height of window")

        ## Set options, then add the job
        self.options_width = 0
        for i, option in enumerate(self.menu):
            option.x = x
            if self.xcenter:
                option.x = (self.width // 2) - (option.width // 2)
            option.y = y
            if self.added.back_button and i == len(self.menu)-1:
                option.y = y + SPACER
            option.onmouseleave = mouseLeave
            option.onmouseenter = mouseEnter
            self.addJob(option.text, option)
            self.options.append(option.text)
            y += option.height
            if option.width > self.options_width:
                self.options_width = option.width

        self.addJob(
                "options_border",
                Jobs.Border3D(
                    self,
                    SPACER/2,
                    self.options_pos[1] - SPACER,
                    self.width - SPACER,
                    self.height - self.options_pos[1],
                    [(40, 40, 40), (90, 90, 90), (90, 90, 90), (40, 40, 40)],
                    SPACER/2,
                    background=MENU_3DBORDER_BACKGROUND,
                    )
                )

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

        ## TODO: Finish this, include key-support in scrolling menus
        if self.menu[item].y + self.menu[item].height + SPACER >= self.height:
            self.scroll(-(self.menu[item].height))

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

    def getOptions(self):
        for menu in self.menu:
            yield menu

    def scroll(self, amount):
        if self.menu[0].y >= self.options_pos[1] and amount > 0:
            return
        if self.menu[-1].y + self.menu[-1].height <= self.height and amount < 0:
            return
        for option in self.getOptions():
            option.y += amount
        Pygame.draw.rect(
                self.screen,
                self.bgcolor,
                (self.options_pos[0], self.options_pos[1], self.options_width, self.height - self.options_pos[1])
                )

    def execOption(self):
        ## Right now each option just runs a function, this may change
        option = self.lookup[self.options[self.getSelectedItem()]]
        option.onmouseclick()

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll(2)
            if event.button == 5:
                self.scroll(-2)

        if event.type == KEYDOWN:
            if event.key == Shared.keymap["menu"]["back"]:
                self.close()
            elif event.key == Shared.keymap["menu"]["down"]:
                self.move(1)
            elif event.key == Shared.keymap["menu"]["up"]:
                self.move(-1)
            elif event.key == Shared.keymap["menu"]["select"]:
                self.execOption()

