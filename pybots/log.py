#!/usr/bin/env python

import os
import sys
from . import vars

header = ""

if os.name == 'e32':
	logfile = os.path.join(vars.SYMBIAN_BASE_DIR, vars.LOGFILE)
else:
	logfile = os.path.join(os.path.dirname(sys.argv[0]), vars.LOGFILE)

def init():
	global logfile
	try:
		open(logfile, "w").close()
	except IOError as e:
		print(e)

def setheader(hdr):
	global header
	header = hdr

def writelog(msg, level=0):
	global logfile
	if vars.OUT_VERBOSITY > level:
		print(msg)

	if vars.FILE_VERBOSITY > level:
		try:
			fp = open(logfile, "a")
			fp.write("%s\n" % msg)
			fp.close()
		except IOError as e:
			print(e)

def major(msg):
	writelog("%s%s" % (header,msg), 0)

def minor(msg):
	writelog("%s%s" % (header,msg), 1)

def trace(msg):
	writelog("%s%s" % (header,msg), 2)

init()

