#!/usr/bin/python2
#-*- coding: utf-8 -*--

FRAMERATE = 25
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SPACER = 10
SOUND_ENABLED = False
HIGHSCORES = 5
UBERCOLOR = (0x70, 0x70, 0x22)
PREVIEW_HEIGHT = 5
PREVIEW_WIDTH = 7
SPED_UP_UPDATEINTERVAL = 2

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

SCREEN_HEIGHT = (BOARD_BLOCKWIDTH * BOARD_HEIGHT) + BOARD_BLOCKWIDTH*2
SCREEN_WIDTH = 450

## TODO: Put font and colorscheme information in JSON files.

GLOBAL_FONT_NAME = "orbitron"
MENU_HEADER_FONT = {
        "name":"orbitron-bold",
        "size":55,
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
        "size":15,
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
CREDITS_COLORSCHEME = { "background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa), "border":(0xaa,0xaa,0xaa), }
ERRORBOX_FONT = MENU_OPTION_FONT
ERRORBOX_COLORSCHEME = { "background":(0x22,0x22,0x22), "font":(0xaa,0xaa,0xaa), "border":(0xaa,0xaa,0xaa), }

# DISPLAY_OPTIONS = FULLSCREEN | DOUBLEBUF | HWSURFACE
DISPLAY_OPTIONS = 0
GHOST_COLOR = (0x29, 0x29, 0x29)

PROJECT_SITE = "https://github.com/UndeadMastodon/Loltris"

SCORES = {
        "tetris": {1: 100, 2: 250, 3: 500, 4: 1500},
        }

EOL = "\ǹ"
