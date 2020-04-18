#!/usr/bin/env python

from pybots import log, bot, bot_loader

bots = bot_loader.load_bots()

for (name, ai, color) in bots:
    b = bot.Bot(name, (0, 0), None, ai, color)
    if b.check_valid():
        log.major("%s -> %d" % (name, b.calc_cost()))
    else:
        log.major("%s -> INVALID" % name)
