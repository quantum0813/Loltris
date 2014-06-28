#!/usr/bin/python2
#-*- coding: utf-8 -*--

## Hardcoded variables, some of these are defaults which can be "overwritten"
## by options in the Settings.json file.

from pygame.locals import *

## The program version (also used in the cxfreeze setup script)
VERSION = "0.5.3"

## Graphics {{{
CENTER_WINDOW = True
FRAMERATE = 32
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SPACER = 10
MAKETETROMINO_OPTION_SPACER = 4
UBERCOLOR = (0x70, 0x70, 0x22) ## Color of the über-tetromino
PREVIEW_HEIGHT = 6 ## Preview window
PREVIEW_WIDTH = 7 ## Preview window
BOARD_BLOCKWIDTH = 20
SCREEN_HEIGHT = SPACER + (BOARD_BLOCKWIDTH * BOARD_HEIGHT) + SPACER
SCREEN_WIDTH = SPACER + (BOARD_WIDTH * BOARD_BLOCKWIDTH) + SPACER + (PREVIEW_WIDTH * BOARD_BLOCKWIDTH) + SPACER
FALLBACK_COLOR = (0xff,0xff,0xff)
MENU_3DBORDER_BACKGROUND = (29,29,29)
MENU_BACKGROUND = (0x22, 0x22, 0x22)
TETRIS_BACKGROUND = (0x22, 0x22, 0x22)
GHOST_COLOR = (0x29, 0x29, 0x29)
# DISPLAY_OPTIONS = FULLSCREEN | DOUBLEBUF | HWSURFACE
DISPLAY_OPTIONS = 0
TITLE_TEXT = "LOLTRIS"
## }}}

## Tetris Gameplay {{{
MOVING_TETROMINO_TIMEOUT = 0.05
MOVE_TETROMINO_TIMEOUT = 0.2
SPED_UP_UPDATEINTERVAL = FRAMERATE * MOVING_TETROMINO_TIMEOUT ## How fast the Tetromino should move when sped up
## These control automatic horizontal movenet (when the block is rotated)
MAX_HORIZONTAL_AUTO_MOVE_LEFT = 2
MAX_HORIZONTAL_AUTO_MOVE_RIGHT = 2
LEVEL_LINES = 20
LEVEL_LINES_INCREASE = 5
UPDATEINTERVAL_DECREASE = FRAMERATE / 10
SCORES = {
        "tetris": {1: 100, 2: 250, 3: 500, 4: 1500},
        }
## }}}

## Sound {{{
SOUND_ENABLED = False
## }}}

## Misc functionality {{{
KEYDOWN_REPEAT_INTERVAL = 20
KEYDOWN_REPEAT_DELAY = 500
HIGHSCORES = 5
## }}}

## Misc internals {{{
LOGLEVEL = 4 ## See Log.loglevel for details on this variable
DISPLAY_FRAMERATE_INTERVAL = 5
JSON_INDENT = 2
EOL = "\ǹ"
PROJECT_SITE = "http://undeadmastodon.github.io/Loltris/"
## }}}

## TODO: Put font and colorscheme information in JSON files.

## Fonts {{{
FALLBACK_FONT_NAME = "orbitron"
MENU_HEADER_FONT = {
        "name":"orbitron-bold",
        "size":50,
        }
MENU_OPTION_FONT = {
        "name":"orbitron",
        "size":20,
        "bold":False,
        }
TETRIS_STATUSBOX_FONT = {
        "name":"orbitron",
        "size":14,
        "bold":False,
        }
HIGHSCORELIST_FONT = {
        "name":"orbitron",
        "size":15,
        "bold":False,
        }
CREDITS_FONT = {
        "name":"freemono",
        "size":15,
        "bold":False,
        }
## }}}

## Colorschemes {{{
MENU_COLORSCHEME = {
        "header": (0xff,0xff,0xff),
        "selected": (0x66,0x66,0x66),
        "background":(0x22,0x22,0x22),
        "option":(0xaa,0xaa,0xaa),
        }
SWITCH_OPTION_COLORS = {
        "background":(0x22,0x22,0x22),
        "font":(0xaa,0xaa,0xaa),
        "checkbox":(0xaa,0xaa,0xaa),
        "on":(0x66,0x66,0x66),
        "off":MENU_COLORSCHEME["background"],
        "border":(0x66,0x66,0x66),
        }
TETRIS_STATUSBOX_COLORSCHEME = {"border":(0x50,0x50,0x50), "font":(0x90,0x90,0x90), "background":(0x22,0x22,0x22)}
HIGHSCORELIST_COLORSCHEME = {"border":(0x50,0x50,0x50), "font":(0xaa,0xaa,0xaa), "background":(0x22,0x22,0x22)}
CREDITS_COLORSCHEME = {"background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa), "border":(0xaa,0xaa,0xaa), }
HIGHSCORE_EXPLORER_STATUSBOX_COLORSCHEME = TETRIS_STATUSBOX_COLORSCHEME
HIGHSCORE_EXPLORER_STATUSBOX_FONT = {
        "name":"orbitron",
        "size":14,
        "bold":False,
        }
ERRORBOX_FONT = MENU_OPTION_FONT
ERRORBOX_COLORSCHEME = { "background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa), "border":(0xaa,0xaa,0xaa), }
## }}}

## Keys that do not directly represent a single character, here are their
## string representations.
NONCHARACTERS = {
        K_LSHIFT: "L-Shift",
        K_RSHIFT: "R-Shift",
        K_RSUPER: "R-Super",
        K_LSUPER: "L-Super",
        K_LALT: "L-Alt",
        K_RALT: "R-Alt",
        K_RCTRL: "R-Ctrl",
        K_LCTRL: "L-Ctrl",
        K_BACKSPACE: "Backspace",
        K_DOWN: "Down",
        K_UP: "Up",
        K_RIGHT: "Right",
        K_RETURN: "Return",
        K_LEFT: "Left",
        K_ESCAPE: "Escape",
        K_PAGEDOWN: "PgDn",
        K_PAGEUP: "PgUp",
        K_TAB: "Tab",
        K_END: "End",
        K_HOME: "Home",
        K_PRINT: "PrntScr",
        K_INSERT: "Insert",
        K_DELETE: "Delete",
        }
