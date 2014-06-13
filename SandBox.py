#!/usr/bin/python

## File for testing out new features

import Core
import Shared
import Jobs
import pygame
from pygame.locals import *
from Globals import *

class SandBox(Core.Game):
    def __init__(self, **kwargs):
        super(SandBox, self).__init__(
                "SandBox", **kwargs
                )

        self.addJob(
                "slider",
                Jobs.Slider(
                    self,
                    "nop",
                    (30, 30),
                    (SCREEN_WIDTH-30, 30),
                    )
                )

        self.running = self.mainLoop

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()
        if event.type == KEYDOWN:
            if event.key == Shared.keymap["menu"]["back"]:
                self.quitGame()

    def mainLoop(self):
        pass

