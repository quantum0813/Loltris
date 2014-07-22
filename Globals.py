#!/usr/bin/python2
#-*- coding: utf-8 -*--

## Hardcoded variables, some of these are defaults which can be "overwritten"
## by options in the Settings.json file.

from pygame.locals import *
import os as OS

## The program version (also used in the cxfreeze setup script)
VERSION = "0.6.0"
## See Log.loglevel for details on this variable
LOGLEVEL = 5

## Framerates {{{
TETRIS_FRAMERATE = 32
CREDITS_FRAMERATE = 24
MENU_FRAMERATE = 24
## }}}

## Network {{{
LAN_GAME_BROADCAST_PORT = 31337
LAN_GAME_BROADCAST_INTERVAL = 1
LAN_GAME_PLAY_PORT = 31338
GAMES_LOOKUP = {
        0: "knockout",
        1: "first_to_n",
        "knockout": 0,
        "first_to_n": 1,
        }
## }}}

## Graphics {{{
CENTER_WINDOW = False
BOARD_WIDTH = 12
BOARD_HEIGHT = 24
SPACER = 10
MAKETETROMINO_OPTION_SPACER = 4
UBERCOLOR = (0x70, 0x70, 0x22) ## Color of the über-tetromino
PREVIEW_HEIGHT = 6 ## Preview window
PREVIEW_WIDTH = 7 ## Preview window
BOARD_BLOCKWIDTH = 25
SCREEN_HEIGHT = SPACER + (BOARD_BLOCKWIDTH * BOARD_HEIGHT) + SPACER
SCREEN_WIDTH = SPACER + (BOARD_WIDTH * BOARD_BLOCKWIDTH) + SPACER + (PREVIEW_WIDTH * BOARD_BLOCKWIDTH) + SPACER
FALLBACK_COLOR = (0xff,0xff,0xff)
TETRIS_3DBORDER_BACKGROUND = (29,29,29)
MENU_3DBORDER_BACKGROUND = (29,29,29)
MENU_BACKGROUND = (0x22, 0x22, 0x22)
TETRIS_BACKGROUND = (0x22, 0x22, 0x22)
GHOST_COLOR = (0x29, 0x29, 0x29)
# DISPLAY_OPTIONS = FULLSCREEN | DOUBLEBUF | HWSURFACE ## High-performence display options
DISPLAY_OPTIONS = 0
TITLE_TEXT = "LOLTRIS" ## Used in main menu
WM_ICON = "favicon.png"
## }}}

## Tetris Gameplay {{{
MOVING_TETROMINO_TIMEOUT = 0.01
MOVE_TETROMINO_TIMEOUT = 0.2
SPED_UP_UPDATEINTERVAL = TETRIS_FRAMERATE * MOVING_TETROMINO_TIMEOUT ## How fast the Tetromino should move when sped up
## These control automatic movement (when the block is rotated)
MAX_HORIZONTAL_AUTO_MOVE = 3
MAX_VERTICAL_AUTO_MOVE = 3
LEVEL_LINES = 20
LEVEL_LINES_INCREASE = 5
UPDATEINTERVAL_DECREASE = TETRIS_FRAMERATE / 10
TETRIS_SCORES = { 1: 100,
                  2: 250,
                  3: 500,
                  4: 1500,
                }
TETRIS_SCORES_OTHER = 9001
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
DISPLAY_TETRIS_FRAMERATE_INTERVAL = 5
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
LAN_GAMES_TABLE_FONT = {
        "name":"orbitron",
        "size":20,
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
        0: u"(null)",
        K_LSHIFT: u"L-Shift",
        K_RSHIFT: u"R-Shift",
        K_RSUPER: u"R-Super",
        K_LSUPER: u"L-Super",
        K_LALT: u"L-Alt",
        K_RALT: u"R-Alt",
        K_RCTRL: u"R-Ctrl",
        K_LCTRL: u"L-Ctrl",
        K_BACKSPACE: u"Backspace",
        K_DOWN: u"Down",
        K_UP: u"Up",
        K_RIGHT: u"Right",
        K_RETURN: u"Return",
        K_LEFT: u"Left",
        K_ESCAPE: u"Escape",
        K_PAGEDOWN: u"PgDn",
        K_PAGEUP: u"PgUp",
        K_TAB: u"Tab",
        K_END: u"End",
        K_HOME: u"Home",
        K_PRINT: u"PrntScr",
        K_INSERT: u"Insert",
        K_DELETE: u"Delete",
        K_SPACE: u"Space",
        }

