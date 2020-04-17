#!/usr/bin/env python

# GUI Parameters
#  Enable/disable GUI
GUI_ENABLED = False
#  Frames-per-second (if GUI is enabled)
GUI_FPS = 10
#  Scale of the gui (i.e. 1.0 means that a 400x300 arena will be displayed
#  with 400x300 pixels)
GUI_SCALE = 1

# The number of steps before the end of the round
ROUND_DURATION = 1000

# Maximum pybot cost available (pybots with higher cost will not be allowed
# to play)
MAX_BOT_COST = 35

# Hit received for generating an exception
EXCEPTION_COST = 1000

# Folder to look for pybot scripts
BOTDIR = 'pybots/bots'

# Verbosity for file and for stdout:
#  0 - no log
#  1 - essential
#  2 - verbose
#  3 - trace
OUT_VERBOSITY = 1
FILE_VERBOSITY = 2

# Logfile (will be truncated at the beginning of every game)
LOGFILE = 'run.log'
