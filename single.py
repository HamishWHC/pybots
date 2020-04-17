#!/usr/bin/env python

import sys

from pybots import log, runner

w = 400
h = 300
walldmg = 0

try:
	w = int(sys.argv[1])
	h = int(sys.argv[2])
	walldmg = int(sys.argv[3])
except:
	log.major("WARNING: Command line is invalid or incomplete")

runner.begin_round(((w, h, walldmg)))
runner.run_round()

