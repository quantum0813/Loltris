#!/usr/bin/python

import Load
import Jobs
import Log
import Matrix
import Core
import Shared
import os
import TetrisGame
import Menus
from Globals import *
from DataTypes import *
from copy import copy

def matrixAddLowerLine(matrix, color):
    matrix_ = [[None for _ in xrange(len(matrix[0]))] for _ in xrange(len(matrix))]
    for row in xrange(len(matrix)):
        for column in xrange(len(matrix[row])):
            try:
                if matrix[row][column]:
                    matrix_[row-1][column] = matrix[row][column]
            except IndexError:
                return None

    ## Add the extra line
    matrix_[len(matrix)-1] = [color for _ in xrange(len(matrix[0]))]
    return matrix_

## XXX: TO BE CONTINUED
# def setAddLowerLine(matrix, color):
#     matrix_ = copy(matrix)
#     for row, colum  in 

class TwoPlayerTetris(Core.Game):
    def __init__(self, *args, **kwargs):
        self.id = "TwoPlayerTetris"
        super(TwoPlayerTetris, self).__init__(
                self.id, *args, fill=True, soundtrack=os.path.join(Load.MUSICDIR, "uprising.ogg"), sound_enabled=SOUND_ENABLED,
                width=SCREEN_WIDTH*2, **kwargs
                )
        self.running = self.mainLoop
        self.addJob("player1_interface", TetrisGame.TetrisInterface(self, SCREEN_WIDTH, SPACER))
        self.addJob("player2_interface", TetrisGame.TetrisInterface(self, SPACER, SPACER, keymap=Shared.keymap["game"]["player2"]))

    def mainLoop(self):
        def handleWinner(*interfaces):
            for interface in interfaces:
                if not interface.jobs.board.update_required and not hasattr(self.jobs, "window_game_over"):
                    ## XXX: LOSER
                    board = interface.jobs.board

                    Log.log("Game over, displaying game state")
                    matrix = [
                            [(x, y) in board.blocks for x in xrange(board.blocks_width)]
                            for y in xrange(board.blocks_height)
                            ]
                    Matrix.put(matrix, f="_")

                    self.addJob("window_game_over",
                            Jobs.TextBox(self, "Yuo An Losar", font={"name": "orbitron-bold", "size": 30, "bold": True},
                                textfit=True, onmouseclick=lambda: game.removeJob("window_game_over"),
                                colors=ERRORBOX_COLORSCHEME, background=True, border=True,
                                padding=6,
                                )
                            )
                    self.jobs.window_game_over.x = interface.x + interface.width//2
                    self.jobs.window_game_over.y = interface.y + interface.height//2 - self.jobs.window_game_over.height//2

            if sum(int(iface.jobs.board.update_required) for iface in interfaces) == 1 and not hasattr(self.jobs, "endtimer"):
                ## XXX: WINNER
                interface = [iface for iface in interfaces if iface.jobs.board.update_required][0]
                self.addJob("window_win",
                        Jobs.TextBox(self, "Yuo An Winrar", font={"name": "orbitron-bold", "size": 30, "bold": True},
                            textfit=True, onmouseclick=lambda: game.removeJob("window_win"),
                            colors=ERRORBOX_COLORSCHEME, background=True, border=True,
                            padding=6,
                            )
                        )
                self.jobs.window_win.x = interface.x + interface.width//2
                self.jobs.window_win.y = interface.y + interface.height//2 - self.jobs.window_win.height//2
                self.addJob("endtimer", Jobs.TimedExecution(self, self.quitGame, seconds=3, anykey=False, timed=True))

        handleWinner(
                self.jobs.player1_interface,
                self.jobs.player2_interface,
                )

    def eventHandler(self, event):
        if event.type == QUIT:
            self.quit()
        if event.type == KEYDOWN:
            if event.key == Shared.keymap["game"]["pause"]:
                self.call(Menus.PauseMenu, sound_enabled=False, caption="Two Player Tetris - Paused")

