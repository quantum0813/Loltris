#!/usr/bin/python

import Shared
import Core
import Load
import Jobs
import TetrisGame
import MakeTetromino
import Log
import pygame as Pygame
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
                ("Highscores", lambda: self.call(HighscoreList, caption="Loltris - Highscores"),),
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
                ("Exit Game", self.quit,),
                ("Exit to main menu", lambda: self.quitGame("MainMenu"),),
                ("Continue", self.quitGame,),
                ]
        self.setupObjects()

## Placeholder, need to add sliders and other stuff to the Menu class
## for an option menu to be doable.
class OptionsMenu(Core.Menu):
    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__("OptionsMenu", header_font=MENU_HEADER_FONT, option_font=MENU_OPTION_FONT, **kwargs)
        self.header = "Options"
        self.menu = [
                ("Crash", lambda: lololololololololol)
                ]
        self.setupObjects()

