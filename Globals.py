#!/usr/bin/python2
#-*- coding: utf-8 -*--

from pygame.locals import *
import pygame as Pygame

FRAMERATE = 30
MOVING_TETROMINO_TIMEOUT = 0.05
MOVE_TETROMINO_TIMEOUT = 0.2
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
# BOARD_WIDTH = 40
# BOARD_HEIGHT = 30
SPACER = 10
MAKETETROMINO_OPTION_SPACER = 4
LOGLEVEL = 4
SOUND_ENABLED = False
HIGHSCORES = 5
UBERCOLOR = (0x70, 0x70, 0x22)
PREVIEW_HEIGHT = 6
PREVIEW_WIDTH = 7
SPED_UP_UPDATEINTERVAL = FRAMERATE * MOVING_TETROMINO_TIMEOUT
JSON_INDENT = 2

## TODO: Need a way to set this, could be done in options, or the player could be asked
##       to input her name whenever she get's on the top scorers list. This seems most
##       appropriate, but would require that I write an InputBox class, shouldn't be
##       particularly difficult.
PLAYER = "Anon"

BOARD_BLOCKWIDTH = 20
LEVEL_LINES = 20
LEVEL_LINES_INCREASE = 5
UPDATEINTERVAL_DECREASE = FRAMERATE / 10
FALLBACK_COLOR = (0xff,0xff,0xff)

SCREEN_HEIGHT = SPACER + (BOARD_BLOCKWIDTH * BOARD_HEIGHT) + SPACER
SCREEN_WIDTH = SPACER + (BOARD_WIDTH * BOARD_BLOCKWIDTH) + SPACER + (PREVIEW_WIDTH * BOARD_BLOCKWIDTH) + SPACER

## TODO: Put font and colorscheme information in JSON files.

GLOBAL_FONT_NAME = "orbitron"
MENU_HEADER_FONT = {
        "name":"orbitron-bold",
        "size":50,
        }
MENU_OPTION_FONT = {
        "name":"orbitron",
        "size":20,
        "bold":False,
        }
MENU_COLORSCHEME = {
        "header": (0xff,0xff,0xff),
        "selected": (0x66,0x66,0x66),
        "background":(0x22,0x22,0x22),
        "option":(0xaa,0xaa,0xaa),
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
        "name":"orbitron",
        "size":15,
        "bold":False,
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
CREDITS_COLORSCHEME = { "background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa), "border":(0xaa,0xaa,0xaa), }
ERRORBOX_FONT = MENU_OPTION_FONT
ERRORBOX_COLORSCHEME = { "background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa), "border":(0xaa,0xaa,0xaa), }

# DISPLAY_OPTIONS = FULLSCREEN | DOUBLEBUF | HWSURFACE
DISPLAY_OPTIONS = 0
GHOST_COLOR = (0x29, 0x29, 0x29)

PROJECT_SITE = "http://undeadmastodon.github.io/Loltris/"

SCORES = {
        "tetris": {1: 100, 2: 250, 3: 500, 4: 1500},
        }

EOL = "\ǹ"

## Keys that do not directly represent a single character
NONCHARACTERS = (
        Pygame.K_LSHIFT,
        Pygame.K_RSHIFT,
        Pygame.K_RSUPER,
        Pygame.K_LSUPER,
        Pygame.K_LALT,
        Pygame.K_RALT,
        Pygame.K_RCTRL,
        Pygame.K_LCTRL,
        Pygame.K_BACKSPACE,
        )

## _ and O are declared to make TITLE_BLOCKS more readable
_ = False
O = True
TITLE_BLOCKS = [
        [O,_,_,_,O,O,O,_,O,_,_,O,O,O,_,O,O,O,_,O,_,O,O,O],
        [O,_,_,_,O,_,O,_,O,_,_,_,O,_,_,O,_,O,_,O,_,O,_,_],
        [O,_,_,_,O,_,O,_,O,_,_,_,O,_,_,O,O,_,_,O,_,_,O,_],
        [O,_,_,_,O,_,O,_,O,_,_,_,O,_,_,O,_,O,_,O,_,_,_,O],
        [O,O,O,_,O,O,O,_,O,O,O,_,O,_,_,O,_,O,_,O,_,O,O,O],
        ]

