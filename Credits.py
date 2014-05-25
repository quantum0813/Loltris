#!/usr/bin/python

import Core
import Jobs
import Load
import os.path
from Globals import *
from pygame.locals import *

class Credits(Core.Game):
    def __init__(self, *args, **kwargs):
        self.id = "Credits"
        super(Credits, self).__init__(self.id, soundtrack=os.path.join(Load.MUSICDIR, "elevator_cat.ogg"), sound_enabled=SOUND_ENABLED, **kwargs)
        self.text = Load.loadCredits()
        self.running = self.mainLoop

        ## Jobs
        self.addJob("text",
                    Jobs.ScrollingText(
                        self, self.text,
                        speed=-1,
                        font=CREDITS_FONT,
                        colors=CREDITS_COLORSCHEME,
                        )
                    )
        self.addJob("endtimer", Jobs.TimedExecution(self.quitGame, timed=False, anykey=True))

    def mainLoop(self):
        if not self.jobs.text.update_required:
            self.quitGame()

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()
