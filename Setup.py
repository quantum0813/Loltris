#!/usr/bin/python

## Things that have to be done on the first run

import Load
import Log
import os.path as Path
import os as OS
import shutil as Shutil

SETUP_FILE = ".set_up"
SETUP_FILE_CONTENTS = """
# This file tells Loltris that everything has been set up,
# do not remove this file unless you want to set up everything
# again (deletes all user-files)
"""

## Initial contents of Scores.dson, an empty array
SCORES_CONTENTS = """so many"""

def remove(path, follow_links=False):
    """
    Acts appropriately to remove a file; be it a directory, link or plain ol' file.
    """
    if not Path.exists(path):
        return
    if Path.isfile(path) or (Path.islink(path) and follow_links):
        OS.remove(path)
        return True
    if Path.isdir(path):
        Shutil.rmtree(path)
        return True
    if Path.islink(path) and not follow_links:
        OS.unlink(path)
        return True
    return

def mkdir(path, overwrite=False):
    """
    Calls OS.mkdir on path, but calls Log.panic in case of an OSError.
    """
    try:
        if overwrite:
            if remove(path):
                Log.debug("Removed directory {}, overwrite".format(repr(path)))
        elif Path.exists(path):
            return

        OS.mkdir(path)
        Log.debug("Created directory {}".format(repr(path)))
    except OSError:
        Log.panic("Unable to create directory `{}'".format(path))

    return True

def mkfile(path, initial="", overwrite=False):
    """
    Creates a new file, overwriting existing files if overwrite is set to True. Calls
    Log.panic in case of an OSError.
    """
    try:
        if overwrite:
            if remove(path):
                Log.debug("Removed file {}, overwrite".format(repr(path)))
        elif Path.exists(path):
            return

        with open(path, "wb") as wf:
            wf.write(initial)
        Log.debug("Created file {}".format(repr(path)))
    except OSError:
        Log.panic("Unable to create file `{}'".format(path))

    return True

def setupFiles():
    """
    Sets up necessary files and directories for Loltris
    """
    if Path.exists(Path.join(Load.DATADIR, SETUP_FILE)):
        return

    Log.log("Running first-time setup")

    mkdir(Load.HIGHSCOREDIR, overwrite=True)
    mkdir(Path.join(Load.HIGHSCOREDIR, "Snapshots"), overwrite=True)

    mkfile(Path.join(Load.HIGHSCOREDIR, "Scores.dson"), initial=SCORES_CONTENTS, overwrite=True)
    ## Finally- if everything was set up successfully- create the SETUP_FILE so Loltris
    ## know that the necessary files/directories have been set up.
    mkfile(Path.join(Load.DATADIR, SETUP_FILE), SETUP_FILE_CONTENTS, overwrite=True)

