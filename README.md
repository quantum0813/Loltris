Loltris
=======

Loltris is a tetris clone written in Python/Pygame, it currently has the following
features.

* Features
  * Tetromino creator
  * Tetris game
    * Preview of next block
    * Status information
    * "Ghostpiece"
  * Highscore list
  * Interactive menus, with mouse support (wow...)
    * Mouse and arrow-keys can be used interchangeably
  * "Über-Tetromino" joke feature that automatically creates a "perfect" tetromino
  * Flipping (flip the blocks)
  * Modifiable keymap

## Screenshots

![Überblock](Screenshots/loltris_uberblock.png)

![Main menu](Screenshots/loltris_mainmenu.png)

## Issues

* Bugs:
  * Inefficient drawing of blocks, draws too much CPU power for a tetris clone.
    * This is partly due to the Python/SDL combination, but can be fixed.
  * Music does not continue playing after another Game instance has started/finished.

* Planed features
  * Options-menu
    * "With sliders and shit"
  * Detailed highscore list
  * Online/multiplayer functionality
    * server/client
