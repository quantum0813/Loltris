#!/usr/bin/python

## Things that have to be done on the first run

import os
import shutil

import Load
import Log

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
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or (os.path.islink(path) and follow_links):
        os.remove(path)
        return True
    if os.path.isdir(path):
        shutil.rmtree(path)
        return True
    if os.path.islink(path) and not follow_links:
        os.unlink(path)
        return True
    return

class FileExistsError(Exception): pass

def mkdir(path, overwrite=False):
    """
    Calls os.mkdir on path, but calls Log.panic in case of an OSError.
    """
    try:
        if overwrite:
            if remove(path):
                Log.notice("Removed directory {!r}, overwrite".format(path))
        elif os.path.exists(path):
            return

        os.makedirs(path)
        Log.notice("Created directory {}".format(repr(path)))
    except OSError as e:
        Log.panic("Unable to create directory `{}'".format(path), exception=e)

    return True

def mkfile(path, initial="", overwrite=False):
    """
    Creates a new file, overwriting existing files if overwrite is set to True. Calls
    Log.panic in case of an OSError.
    """
    try:
        if overwrite:
            if remove(path):
                Log.notice("Removed file {}, overwrite".format(repr(path)))
        elif os.path.exists(path):
            return

        with open(path, "wb") as wf:
            wf.write(initial)
        Log.notice("Created file {}".format(repr(path)))
    except OSError as e:
        Log.panic("Unable to create file `{}'".format(path), exception=e)

    return True

def setupFiles():
    """
    Sets up necessary files and directories for Loltris
    """
    if os.path.exists(os.path.join(Load.DATADIR, SETUP_FILE)):
        return

    Log.log("Running first-time setup")

    # mkdir(Load.HIGHSCOREDIR, overwrite=True)
    mkdir(os.path.join(Load.DATADIR))
    mkdir(os.path.join(Load.SNAPSHOTDIR))
    for directory in Load.LOCALDIRS:
        Log.notice("copying {} to {}".format(os.path.join(Load.INSTALL_DATA_LOCAL, directory), os.path.join(Load.DATADIR, directory)))
        shutil.copytree(os.path.join(Load.INSTALL_DATA_LOCAL, directory), os.path.join(Load.DATADIR, directory))

    mkfile(os.path.join(Load.HIGHSCOREDIR, "Scores.dson"), initial=SCORES_CONTENTS)
    ## Finally- if everything was set up successfully- create the SETUP_FILE so Loltris
    ## know that the necessary files/directories have been set up.
    mkfile(os.path.join(Load.DATADIR, SETUP_FILE), SETUP_FILE_CONTENTS, overwrite=True)

