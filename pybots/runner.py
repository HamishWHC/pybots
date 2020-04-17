#!/usr/bin/env python

from . import arena, log, vars, bot, botloader, tkgui
import os

ar = None
bots = None
arenalist = []

def begin_round(ar_data=None):
	global bots, ar

	if (bots == None):
		begin_tournament()

	try:
		if (ar_data==None):
			ar_data = arenalist.pop()
		ar = arena.arena(ar_data[0], ar_data[1], ar_data[2])
	except IndexError:
		log.major("Running in default arena")
		ar = arena.arena()

	for (name, ai, color) in bots:
		b = bot.bot(name, (0, 0), ar, ai, color)
		if not b.check_valid():
			log.major("Bot %s is disqualified (invalid hardware)" % name)
			continue
		if b.calc_cost() > vars.MAX_BOT_COST:
			log.major("Bot %s is disqualified (hardware too expensive)" % name)
			continue
		ar.addbot(b)

def runstep():
	global ar, step
	log.setheader("%4d - " % step)
	ar.step()
	ar.dump()
	step += 1
	log.setheader("")
	return not(ar.is_over()) and (step < vars.ROUND_DURATION)

def run():
	while runstep():
		if os.name == 'e32':
			e32.ao_yield()

def run_round():
	global gui, ar, step

	gui = None

	if vars.GUI_ENABLED:
		gui = tkgui.gui()

	step = 0

	if gui:
		gui.startgui(ar, runstep)
	else:
		run()

	return ar.dump_winners()

def begin_tournament(arene=[], rpa=1):
	global bots, arenalist
	bots = botloader.load_bots()

	for a in arene:
		if len(a) == 3:
			for i in range(rpa):
				arenalist.append(a)

def run_tournament():
	global bots, arenalist

	wins = {}

	while len(arenalist) > 0:
		begin_round()
		w = run_round()
		for bw in w:
			try:
				wins[bw] = wins[bw] + 1
			except KeyError:
				wins[bw] = 1

	log.major("Tournament results:")
	maxwin = 0
	winners = []
	for (bot,win) in wins.items():
		log.major("%s -> %d" % (bot, win))
		if win > maxwin:
			winners = [bot]
		elif win == maxwin:
			winners.append(bot)

	return winners

