#!/usr/bin/python

## Things that have to be done on the first run

import Load
import Log
import os.path as Path

SETUP_FILE = ".set_up"

SCORES_CONTENTS = """
<scores>
</scores>
"""

def setupFiles():
    if Path.exists(Path.join(Load.DATADIR, SETUP_FILE)):
        return

    Log.log("Setting up files for Loltris")

    with open(Path.join(Load.DATADIR, SETUP_FILE), "w") as wf:
        wf.write("This file just tells Loltris that everything has been set up," + \
                 "do not remove this file unless you want to set up everything" + \
                 "again (deletes all user-files like scores)")

    with open(Path.join(Load.HIGHSCOREDIR, "Scores.xml"), "w") as wf:
        wf.write(SCORES_CONTENTS)
