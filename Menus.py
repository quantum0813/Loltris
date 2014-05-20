#!/usr/bin/python

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
from pygame.locals import *
from Globals import *

class MenuAction(object):
    def __init__(self, seq, text, function):
        self.text = text
        self.function = function
        self.seq = seq

class MainMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__("MainMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, isroot=True, **kwargs)
        self.header = "Loltris"
        self.menu = [
                ("Start Game", self.startTetrisGame,),
                ("Options", lambda: self.call(OptionsMenu, caption="Loltris - Options"),),
                ("Creator", lambda: self.call(MakeTetromino.MakeTetromino, caption="Loltris - Creator"),),
                ("Highscores", lambda: self.call(HighscoreExplorer.HighscoreList, caption="Loltris - Highscores"),),
                ("Exit", self.quit,),
                ]
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
                         y=self.jobs.header.y+self.jobs.header.height+10, textfit=True,
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
        super(PauseMenu, self).__init__("PauseMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, isroot=True, **kwargs)
        self.header = "Pause"
        self.menu = [
                ("Continue", self.quitGame),
                ("Exit to main menu", lambda: self.quitGame("MainMenu")),
                ("Exit Game", self.quit),
                ]
        self.setupObjects()

## Placeholder, need to add sliders and other stuff to the Menu class
## for an option menu to be doable.
class OptionsMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__("OptionsMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
        self.header = "Options"
        self.options = Load.loadOptions()
        self.menu = [
                ("Keymaps", lambda: self.call(KeymapMenu, caption=self.caption))
                ]
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

class KeymapMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(KeymapMenu, self).__init__("KeymapMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
        self.header = "Pause"
        self.menu = [
                ("Tetris", lambda: self.call(self.Tetris)),
                ("Menu", lambda: self.call(self.Menu)),
                ]
        self.setupObjects()

    class Tetris(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Tetris, self).__init__("PauseMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
            self.header = "Tetris keymap"
            self.menu = [
                    ("Rotate left", lambda: None)
                    ]
            self.setupObjects()
    class Menu(Core.Menu):
        def __init__(self, **kwargs):
            super(KeymapMenu.Menu, self).__init__("Menu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
            self.header = "Menu keymap"
            self.menu = [
                    ("Move down", lambda: None)
                    ]
            self.setupObjects()


