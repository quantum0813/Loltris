#!/usr/bin/python2
#-*- coding: utf-8 -*-

## =====================================================================
## Menus for Loltris
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

import Shared
import BlockText
import Core
import Load
import Jobs
import Log
import Factory
import Credits
import Save
import Matrix
import Utils
import webbrowser as Webbrowser
import os.path as Path
from functools import *
from pygame.locals import *
from Globals import *
from DataTypes import *

## Games
import HighscoreExplorer
import TetrisGame
import MakeTetromino
import SandBox
import TwoPlayerTetrisGame
# import LANTetrisGame

class MainMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(
                "MainMenu", onHeaderClick=lambda: Webbrowser.open(PROJECT_SITE),
                header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, isroot=True, xcenter=True,
                soundtrack=Path.join(Load.MUSICDIR, "jazz_cat_infinite_loop_cut.ogg"), sound_enabled=SOUND_ENABLED, **kwargs)

        self.title_blocks = BlockText.render(TITLE_TEXT, font=Load.loadBlockFont("standard"))
        blockwidth = (self.width) // len(self.title_blocks[0])
        Log.debug("title_board.blockwidth = {}".format(blockwidth))
        self.addJob("title_board",
                    Jobs.Board(
                        self,
                        y=SPACER,
                        height=len(self.title_blocks),
                        width=len(self.title_blocks[0]),
                        blockwidth=blockwidth,
                        bgcolor=self.bgcolor,
                        queue=100,
                        draw_grid=False,
                        draw_border=False,
                        )
                    )
        self.jobs.title_board.x = (self.width // 2) - (self.jobs.title_board.width // 2)
        for x, y in Matrix.matrixToSet(self.title_blocks):
            self.jobs.title_board.blocks[(x, y)] = (0xaa,0xaa,0xaa)
        self.options_pos[1] = self.jobs.title_board.y + self.jobs.title_board.height + SPACER*2

        self.menu = Factory.textBoxes([
                ("Single Player", lambda: self.call(TetrisGame.TetrisGame, caption="Loltris")),
                ("Two Player", lambda: self.call(TwoPlayerTetrisGame.TwoPlayerTetris, caption="Loltris - Two Player")),
                ("LAN Play", lambda: self.call(LANTetrisGame.LANMenu, caption="Loltris - LAN play")),
                ("Options", lambda: self.call(OptionsMenu, caption="Loltris - Options")),
                ("Creative", lambda: self.call(MakeTetromino.MakeTetromino, caption="Loltris - Creator")),
                ("Scores", lambda: self.call(HighscoreExplorer.HighscoreList, caption="Loltris - Highscores")),
                ("Credits", lambda: self.call(Credits.Credits, caption="Loltris - Credits")),
                ("Homepage", lambda: Webbrowser.open(PROJECT_SITE)),
                ("SandBox", lambda: self.call(SandBox.SandBox, caption="Loltris - SandBox")),
                ("Exit", self.quit),
                ],
                self,
                font=MENU_OPTION_FONT,
                fill=MENU_3DBORDER_BACKGROUND,
                xcenter=True,
                colors={
                    "background":self.colorscheme["background"],
                    "font":self.colorscheme["option"],
                    },
                )
        self.setupObjects()
        #self.loadHighscores()
        ## XXX: Temporary bugfix, scroll_filler is drawn on every frame while the board is not.
        del self.jobs.scroll_filler

    def loadHighscores(self):
        """ Load scores from disk, then add the highscorelist job to see them """
        self.highscores = Load.loadHighscores(top=HIGHSCORES)
        Log.debug("Loaded new highscores from disk, displaying below")
        Log.dump("".join(["{}: {}\n".format(d["name"], d["score"]) for d in self.highscores]))
        if self.highscores:
            self.addJob(
                     "highscorelist",
                     Jobs.TextBox(
                         self,
                         ( "Top {} scores\n\n".format(HIGHSCORES) + ## Title
                           "".join(["{}: {}\n".format(x["name"], x["score"]) for x in self.highscores]) + ## The scores
                           ("\n" * (HIGHSCORES - len(self.highscores))) ## Empty lines
                           ),
                         y=self.menu[0].y+1,
                         textfit=True,
                         colors=HIGHSCORELIST_COLORSCHEME,
                         font=HIGHSCORELIST_FONT,
                         border=True,
                         background=True,
                         )
                    )
            ## The highscore-list should be 5 pixels from the right edge
            self.jobs.highscorelist.x = SCREEN_WIDTH - self.jobs.highscorelist.width - 5

    def launchTetrisGame(self):
        self.call(TetrisGame.TetrisGame, caption="Loltris")
        # self.loadHighscores()

    def eventHandler(self, event):
        super(MainMenu, self).eventHandler(event)
        if event.type == KEYDOWN:
            if event.key == K_TAB:
                self.addJob(
                        "input",
                        Jobs.InputBox(self, "Input: ")
                        )

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
                fill=MENU_3DBORDER_BACKGROUND,
                xcenter=True,
                )
        self.setupObjects()
        self.running = self.mainLoop

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
                fill=MENU_3DBORDER_BACKGROUND,
                xcenter=True,
                )

        ## >inb4 immature jokes
        def turnOn(option, options):
            Log.debug(option)
            if options.get(option) != None:
                Log.warning("Turning on non-existent option: {}".format(repr(option)))
            options[option] = True
            Save.saveOptions()
        def turnOff(option, options):
            Log.debug(option)
            if options.get(option) != None:
                Log.warning("Turning off non-existent option: {}".format(repr(option)))
            options[option] = False
            Save.saveOptions()

        self.menu.extend(
                Factory.basicSwitches([
                    ("Uber-Tetromino", "uber_tetromino"),
                    ("Flip tetromino", "flip_tetromino"),
                    ], self, turnOn, turnOff, Shared.options["gameplay"],
                    font=MENU_OPTION_FONT,
                    colors=SWITCH_OPTION_COLORS,
                    boxwidth=8,
                    box_center=True,
                    fill=MENU_3DBORDER_BACKGROUND,
                    )
                )

        self.setupObjects()

    class Graphics(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Graphics, self).__init__("GraphicsMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
            ## >inb4 immature jokes
            def turnOn(option, options):
                options[option] = True
                Save.saveOptions()
            def turnOff(option, options):
                options[option] = False
                Save.saveOptions()

            self.menu = \
                Factory.basicSwitches([
                    ("Fullscreen", "fullscreen"),
                    ], self, turnOn, turnOff, Shared.options["gameplay"],
                    font=MENU_OPTION_FONT,
                    colors=SWITCH_OPTION_COLORS,
                    boxwidth=8,
                    box_center=True,
                    fill=MENU_3DBORDER_BACKGROUND,
                    )

## Generates a mainloop for getting a single character.
## Used in KeymapMenu.*
def getKeyLoop(self, keys):
    if not self.jobs.input_box.update_required:
        Log.debug("Setting key {} to activate {}".format(Utils.keyToString(self.jobs.input_box.value), self.getting))
        keys[self.getting] = self.jobs.input_box.value
        self.removeJob("input_box")
        Save.saveKeymap()
        ## Restore
        self.running = self.mainLoop

## Sets the appropriate values for setting a key in a keymap.
def modifyKeymap(self, keys, getting):
    self.addJob("input_box", Jobs.GetKeyBox(self, "Press key for {}".format(getting), font=MENU_OPTION_FONT, colors=SWITCH_OPTION_COLORS, queue=self.menu[0].queue+1))
    self.getting = getting
    self.running = partial(getKeyLoop, self, keys)

class KeymapMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(KeymapMenu, self).__init__("KeymapMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
        self.header = "Keymaps"
        self.menu = Factory.textBoxes([
                ("Tetris", lambda: self.call(self.Tetris, caption="Loltris - Tetris keymap")),
                ("Menu", lambda: self.call(self.Menu, caption="Loltris - Menu keymap")),
                ], self, font=MENU_OPTION_FONT, colors={"background":self.colorscheme["background"],
                                                        "font":self.colorscheme["option"], },
                fill=MENU_3DBORDER_BACKGROUND,
                xcenter=True,
                )
        self.setupObjects()
        self.getting = None

    class Tetris(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Tetris, self).__init__("KeymapMenu.Tetris", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
            self.header = "Tetris-map"
            self.menu = Factory.textBoxes(
                    [("Player 1", lambda: self.call(self.Player1, caption="Loltris - Tetris player 1 keymap")),
                     ("Player 2", lambda: self.call(self.Player2, caption="Loltris - Tetris player 2 keymap")),
                    ],
                    self,
                    font=MENU_OPTION_FONT,
                    colors={"background":self.colorscheme["background"], "font":self.colorscheme["option"]},
                    fill=MENU_3DBORDER_BACKGROUND,
                    xcenter=True,
                    )
            self.menu.extend(Factory.variableTextBoxes(
                    [( action.replace("_", " ").capitalize() + ": {key}",
                       ## Nested lambdas are used here to cirumvent an issue with python closures. (http://code.activestate.com/recipes/502271/)
                       ## Basically if you don't nest the lambdas, you will end up with every single functions having the last action in
                       ## the list of dictionary keys.
                       {"key": (lambda action_: lambda _: Utils.keyToString(Shared.keymap["game"][action_]))(action) },
                       lambda: modifyKeymap(self, Shared.keymap["game"], action))
                       for action in Shared.keymap["game"]
                       if isinstance(Shared.keymap["game"][action], int) ## Skip the player1 and player2 sub-dictionaries
                       ],
                    self,
                    font=MENU_OPTION_FONT,
                    colors={"background":self.colorscheme["background"], "font":self.colorscheme["option"]},
                    fill=MENU_3DBORDER_BACKGROUND,
                    xcenter=True,
                    ))
            self.setupObjects()

        class Player1(Core.Menu):
            def __init__(self, **kwargs):
                super(KeymapMenu.Tetris.Player1, self).__init__(
                        "KeymapMenu.Tetris.Player1", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
                self.header = "Player1 Keymaps"
                self.menu.extend(Factory.variableTextBoxes(
                        [( action.replace("_", " ").capitalize() + ": {key}",
                           ## Nested lambdas are used here to cirumvent an issue with python closures. (http://code.activestate.com/recipes/502271/)
                           ## Basically if you don't nest the lambdas, you will end up with every single functions having the last action in
                           ## the list of dictionary keys.
                           {"key": (lambda action_: lambda _: Utils.keyToString(Shared.keymap["game"]["player1"][action_]))(action) },
                           (lambda action_: lambda: modifyKeymap(self, Shared.keymap["game"]["player1"], action_))(action),
                           )
                           for action in Shared.keymap["game"]["player1"]
                           ],
                        self,
                        font=MENU_OPTION_FONT,
                        colors={"background":self.colorscheme["background"], "font":self.colorscheme["option"]},
                        fill=MENU_3DBORDER_BACKGROUND,
                        xcenter=True,
                        ))
                self.setupObjects()

        class Player2(Core.Menu):
            def __init__(self, **kwargs):
                super(KeymapMenu.Tetris.Player2, self).__init__(
                        "KeymapMenu.Tetris.Player2", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs)
                self.header = "Player2 Keymaps"
                self.menu.extend(Factory.variableTextBoxes(
                        [( action.replace("_", " ").capitalize() + ": {key}",
                           ## Nested lambdas are used here to cirumvent an issue with python closures. (http://code.activestate.com/recipes/502271/)
                           ## Basically if you don't nest the lambdas, you will end up with every single functions having the last action in
                           ## the list of dictionary keys.
                           {"key": (lambda action_: lambda _: Utils.keyToString(Shared.keymap["game"]["player2"][action_]))(action) },
                           (lambda action_: lambda: modifyKeymap(self, Shared.keymap["game"]["player2"], action_))(action),
                           )
                           for action in Shared.keymap["game"]["player2"]
                           ],
                        self,
                        font=MENU_OPTION_FONT,
                        colors={"background":self.colorscheme["background"], "font":self.colorscheme["option"]},
                        fill=MENU_3DBORDER_BACKGROUND,
                        xcenter=True,
                        ))
                self.setupObjects()

    class Menu(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Menu, self).__init__(
                    "KeymapMenu.Menu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, xcenter=True, **kwargs
                    )
            self.header = "Menu-map"
            self.menu = Factory.variableTextBoxes(
                [( action.replace("_", " ").capitalize() + ": {key}",
                   ## Nested lambdas are used here to cirumvent an issue with python closures. (http://code.activestate.com/recipes/502271/)
                   ## Basically if you don't nest the lambdas, you will end up with every single functions having the last action in
                   ## the list of dictionary keys.
                   {"key": (lambda action_: lambda _: Utils.keyToString(Shared.keymap["menu"][action_]))(action) },
                   lambda: modifyKeymap(self, Shared.keymap["menu"], action))
                   for action in Shared.keymap["menu"] ],
                self,
                font=MENU_OPTION_FONT,
                colors={
                    "background":self.colorscheme["background"],
                    "font":self.colorscheme["option"],
                    },
                fill=MENU_3DBORDER_BACKGROUND,
                xcenter=True,
                )
            self.setupObjects()

