#!/usr/bin/python

import Core
import Shared
import pygame as Pygame
from pygame.locals import *
from Globals import *

class HighscoreList(Core.Game):
    def __init__(self, top=HIGHSCORES, *args, **kwargs):
        super(HighscoreList, self).__init__("HighscoreList", *args, **kwargs)
        self.running = self.mainLoop

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()

    def mainLoop(self):
        pass

