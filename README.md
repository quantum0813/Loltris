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
  * Menus
  * "Über-Tetromino" joke feature that automatically creates a "perfect" tetromino
  * Flipping (flip the blocks)

* The following bugs:
  * Inefficient drawing of blocks, draws too much CPU power for a tetris clone.
    * This is partly due to the Python/SDL combination, but can be fixed.
  * Music does not continue playing after another Game instance has started/finished.

* Planed features
  * Options-menu
    * "With sliders and shit"
  * Detailed highscore list
  * Online/multiplayer functionality
    * server/client
  * Modifiable keymap
