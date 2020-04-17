#!/usr/bin/env python

import os
import sys
import re

from . import log, vars

rexp_import1 = re.compile("import\\s*([a-zA-Z0-9]*)[^A-Za-z0-9]", re.I + re.S + re.M)
rexp_import2 = re.compile("from\\s*([a-zA-Z0-9]*)\\s*import", re.I + re.S + re.M)

valid_import = [
	'util',
	'random',
	'math',
	'pybots'
]

def readfile(f):
	fp = open(f,"r")
	buf = fp.read()
	fp.close()
	return buf

def botdir():
	return os.path.join(os.path.dirname(sys.argv[0]), os.path.normpath(vars.BOTDIR))

def getcolor(idx):
	colors = [
		(0x00, 0xff, 0x00),
		(0x00, 0x00, 0xff),
		(0xff, 0xff, 0x00),
		(0x00, 0xff, 0xff),
		(0xff, 0x00, 0xff),
		(0xff, 0x80, 0x00),
		(0x80, 0x00, 0xff),
		(0x80, 0x80, 0x80)
	]
	return colors[idx % len(colors)]

def load_bots():
	direction = botdir()
	if not direction in sys.path:
		sys.path.append(direction)

	ret = []
	coloridx = 0

	for f in filter(lambda x: x[-3:].lower() == '.py', os.listdir(direction)):
		name = f[:-3]

		if name in valid_import:
			log.major("Bot %s has an invalid name" % name)
			continue

		buf = readfile(os.path.join(direction,f))

		valid = True
		imp = rexp_import1.findall(buf) + rexp_import2.findall(buf)
		for i in imp:
			if not i in valid_import:
				log.major("Bot %s contains invalid import (%s)" % (name, i))
				valid = False
				break

		if not valid:
			continue

		try:
			exec("import %s" % name)
			ret.append((name, eval("%s.bot()" % name), getcolor(coloridx)))
			coloridx += 1
		except Exception as e:
			log.major("Loading bot %s failed: %s" % (name, e))

	return ret
