## cx_freeze setup script for Loltris, auto-generated using cxfreeze

from cx_Freeze import setup, Executable
from Globals import *

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Loltris.py', base=base)
]

setup(name='Loltris',
      version = VERSION,
      description = 'Tetris clone',
      options = dict(build_exe = buildOptions),
      executables = executables)
