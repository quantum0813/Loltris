#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Menus for Loltris
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

import Shared
import Core
import Load
import Jobs
import TetrisGame
import MakeTetromino
import Log
import pygame as Pygame
import HighscoreExplorer
import sys as Sys
import Factory
import webbrowser as Webbrowser
import os.path as Path
import Credits
import Save
from pygame.locals import *
from Globals import *

## TODO: You know what would be cool? A DSL for doing this, may do that later.

class MainMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(
                "MainMenu", onHeaderClick=lambda: Webbrowser.open(PROJECT_SITE),
                header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, isroot=True,
                soundtrack=Path.join(Load.MUSICDIR, "jazz_cat.ogg"), sound_enabled=SOUND_ENABLED, **kwargs)
        self.header = "Loltris"
        self.menu = Factory.textBoxes([
                ("Start Game", self.startTetrisGame),
                ("Options", lambda: self.call(OptionsMenu, caption="Loltris - Options")),
                ("Creative", lambda: self.call(MakeTetromino.MakeTetromino, caption="Loltris - Creator")),
                ("Highscores", lambda: self.call(HighscoreExplorer.HighscoreList, caption="Loltris - Highscores")),
                ("Credits", lambda: self.call(Credits.Credits, caption="Loltris - Credits")),
                ("Exit", self.quit),
                ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                        "font":self.colorscheme["option"], },
                )
        self.highscores = Load.loadHighscores(top=HIGHSCORES)
        self.setupObjects()
        if self.highscores:
            self.addJob(
                     "highscorelist",
                     Jobs.TextBox(
                         self,
                         ( "Top {} scores\n\n".format(HIGHSCORES) + ## Title
                           "".join(["{}: {}\n".format(x["name"], x["score"]) for x in self.highscores]) + ## The scores
                           ("\n" * (HIGHSCORES - len(self.highscores))) ## Empty lines
                           ),
                         y=self.jobs.header.y+self.jobs.header.height+10,
                         textfit=True,
                         colors={
                             "background":self.colorscheme["background"],
                             "font":self.colorscheme["option"],
                             "border": (0xaa,0xaa,0xaa),
                             },
                         font=HIGHSCORELIST_FONT,
                         border=True,
                         background=True,
                         )
                    )
            ## 5 pixels from the right edge
            self.jobs.highscorelist.x = SCREEN_WIDTH - self.jobs.highscorelist.width - 5

    def startTetrisGame(self):
        self.call(TetrisGame.TetrisGame, caption="Loltris", player_name=PLAYER)
        self.highscores = Load.loadHighscores(top=HIGHSCORES)

class PauseMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(PauseMenu, self).__init__("PauseMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, isroot=True, xcenter=True, **kwargs)
        self.header = "Pause"
        self.menu = Factory.textBoxes([
                ("Continue", self.quitGame),
                ("Exit to main menu", lambda: self.quitGame("MainMenu")),
                ("Exit Game", self.quit),
                ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                        "font":self.colorscheme["option"], },
                )
        self.setupObjects()

## Placeholder, need to add sliders and other stuff to the Menu class
## for an option menu to be doable.
class OptionsMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__("OptionsMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
        self.header = "Options"
        self.options = Load.loadOptions()
        self.menu = Factory.textBoxes([
                ("Keymaps", lambda: self.call(KeymapMenu, caption=self.caption)),
                ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                        "font":self.colorscheme["option"], },
                )

        ## >inb4 immature jokes
        def turnOn(option):
            Log.debug(option)
            if not Shared.options.get(option):
                Log.warning("Turning on non-existent option: {}".format(repr(option)))
            Shared.options[option] = True
            Save.saveOptions()
        def turnOff(option):
            Log.debug(option)
            if not Shared.options.get(option):
                Log.warning("Turning off non-existent option: {}".format(repr(option)))
            Shared.options[option] = None
            Save.saveOptions()

        self.menu.extend(
                Factory.basicSwitches([
                    ("Uber-Tetromino", "uber_tetromino"),
                    ("Flip tetromino", "flip_tetromino"),
                    ], self, turnOn, turnOff, Shared.options,
                    font=MENU_OPTION_FONT,
                    colors=SWITCH_OPTION_COLORS,
                    boxwidth=8,
                    box_center=True,
                    )
                )

        self.setupObjects()

        # ## XXX: TEST CODE
        # self.addJob("test",
        #             Jobs.Switch(
        #                 self,
        #                 "Option",
        #                 box_center=True,
        #                 boxwidth=8,
        #                 whenon=lambda: Log.log("OPTION ENABLED"),
        #                 whenoff=lambda: Log.log("OPTION DISABLED"),
        #                 x=0,
        #                 y=200,
        #                 font=MENU_OPTION_FONT,
        #                 colors={
        #                     "background":(0x22,0x22,0x22),
        #                     "font":(0xaa,0xaa,0xaa),
        #                     "checkbox":(0xaa,0xaa,0xaa),
        #                     "inside":(0x66,0x66,0x66),
        #                     "border":(0x66,0x66,0x66)
        #                     }
        #                 )
        #             )


## Closure that generates a mainloop for getting a single character
## used in KeymapMenu.*
def getKeyLoop(self, keys):
    ## Will act just like a class method when called with no arguments
    def inner():
        if not self.jobs.input_box.update_required:
            keys[self.getting] = self.jobs.input_box.value
            self.removeJob("input_box")
            ## Restore
            self.running = self.mainLoop
    return inner

## Sets the appropriate values for setting a key in a keymap.
def getKey(self, keys, getting):
    self.addJob("input_box", Jobs.GetKeyBox(self, "Press any key", font=MENU_OPTION_FONT, colors=SWITCH_OPTION_COLORS))
    self.getting = getting
    self.running = getKeyLoop(self, keys)

class KeymapMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(KeymapMenu, self).__init__("KeymapMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
        self.header = "Keymaps"
        self.menu = Factory.textBoxes([
                ("Tetris", lambda: self.call(self.Tetris)),
                ("Menu", lambda: self.call(self.Menu)),
                ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                        "font":self.colorscheme["option"], },
                )
        self.setupObjects()
        self.getting = None

    class Tetris(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Tetris, self).__init__("PauseMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
            self.header = "Tetris keymap"
            self.menu = Factory.textBoxes([
                    ("Rotate left", lambda: getKey(self, Shared.keymap["game"], "rotate_left")),
                    ("Pause", lambda: getKey(self, Shared.keymap["game"], "pause")),
                    ("Speed up", lambda: getKey(self, Shared.keymap["game"], "speed_up")),
                    ("Move left", lambda: getKey(self, Shared.keymap["game"], "move_left")),
                    ("Move right", lambda: getKey(self, Shared.keymap["game"], "move_right")),
                    ("Drop down", lambda: getKey(self, Shared.keymap["game"], "drop_down")),
                    ("Rotate right", lambda: getKey(self, Shared.keymap["game"], "rotate_right")),
                    ("Reverse", lambda: getKey(self, Shared.keymap["game"], "reverse")),
                    ("Spawn Uber-Tetromino", lambda: getKey(self, Shared.keymap["game"], "uber_tetromino")),
                    ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                            "font":self.colorscheme["option"], },
                    )
            self.setupObjects()

    class Menu(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Menu, self).__init__("Menu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
            self.header = "Menu keymap"
            self.menu = Factory.textBoxes([
                    ("Move down", lambda: getKey(self, Shared.keymap["game"], "down")),
                    ("Move up", lambda: getKey(self, Shared.keymap["game"], "up")),
                    ("Select", lambda: getKey(self, Shared.keymap["game"], "select")),
                    ("Go back", lambda: getKey(self, Shared.keymap["game"], "back")),
                    ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                            "font":self.colorscheme["option"], },
                    )
            self.setupObjects()

