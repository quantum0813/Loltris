#!/usr/bin/python

import Core
import Jobs
import Load
import Matrix
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
                        fill=MENU_BACKGROUND,
                        )
                    )
        ## TODO: For this to be possible, Jobs.ScrollingText needs to stop drawing itself when it reaches a certain point,
        ##       it needs a y-coordinate where the text starts to disappear.
        # blockwidth = (self.width) // len(TITLE_BLOCKS[0])
        # self.addJob("title_board",
        #             Jobs.Board(
        #                 self,
        #                 y=SPACER,
        #                 height=len(TITLE_BLOCKS),
        #                 width=len(TITLE_BLOCKS[0]),
        #                 blockwidth=blockwidth,
        #                 bgcolor=self.bgcolor,
        #                 queue=100,
        #                 draw_grid=False,
        #                 draw_border=False,
        #                 )
        #             )
        # self.jobs.title_board.x = (self.width // 2) - (self.jobs.title_board.width // 2)
        # for x, y in Matrix.matrixToSet(TITLE_BLOCKS):
        #     self.jobs.title_board.blocks[(x, y)] = (0xaa,0xaa,0xaa)

        self.addJob("endtimer", Jobs.TimedExecution(self.quitGame, timed=False, anykey=True))

    def mainLoop(self):
        if not self.jobs.text.update_required:
            self.quitGame()

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()
