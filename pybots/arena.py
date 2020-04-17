#!/usr/bin/env python

from . import log, util

import random

random.seed()

class arena:
	def __init__(self, w=400, h=300, walldmg=0):
		self.bots = []
		self.shots = []

		self.width = w
		self.height = h
		self.wallpower = walldmg

		self.shots2remove = []
		self.bots2goback = []
		self.bots2remove = []

	def check_random_pos(self, pos, radius):
		if (not(self.inside(pos, radius))):
			return False
		else:
			for b in self.bots:
				if b.collide(pos, radius):
					return False
		return True

	def get_random_pos(self, radius=0):
		redo = True
		tries = 0
		while redo and tries < 100:
			redo = False
			x = radius + random.random() * (self.width - 2*radius)
			y = radius + random.random() * (self.height - 2*radius)
			pos = (x, y)
			if not(self.check_random_pos(pos, radius)):
				redo = True
			tries += 1

		if redo:
			# Random positioning failed... see if we can find anyway a good
			# starting position
			for x in range(radius, self.width - radius):
				for y in range(radius, self.height - radius):
					pos = (x, y)
					if not(self.check_random_pos(pos, radius)):
						redo = True
					else:
						break
				if not(redo):
					break

		if redo:
			raise Exception("Arena is too small")

		return pos

	def addbot(self, bot, recalc_pos=True):
		if recalc_pos:
			bot.pos = self.get_random_pos(bot.size)
		self.bots.append(bot)

	def addshot(self, shot):
		self.shots.append(shot)

	def removebot(self, bot):
		self.bots2remove.append(bot)

	def removeshot(self, shot):
		self.shots2remove.append(shot)


	def inside(self, pos, size=0):
		return (pos[0] >= size) and (pos[1] >= size) and (pos[0] <= self.width - size) and (pos[1] <= self.height - size)

	def moveshots(self):
		for s in self.shots:
			s.move()
			if (not(self.inside(s.pos))):
				self.removeshot(s)

	def movebots(self):
		for b in self.bots:
			b.move()
			if (not(self.inside(b.pos, b.size))):
				log.minor("bot %s hits arena wall" % b.name)
				b.hit(self.wallpower)
				self.bots2goback.append(b)


	def check_collision(self):
		for s in self.shots:
			for b in self.bots:
				if s.owner == b:
					continue

				if b.collide(s.pos, 0):
					log.minor("%s hit %s" % (s.owner.name, b.name))
					b.hit(s.power)
					self.shots2remove.append(s)
					

		for b1 in self.bots:
			for b2 in self.bots:
				if (b1 == b2):
					continue

				if (b1.collide(b2.pos, b2.size)):
					log.minor("%s collided with %s" % (b1.name, b2.name))
					b2.hit(b1.armour)
					self.bots2goback.append(b1)
					self.bots2goback.append(b2)


	def reactions(self):
		for b in self.bots2goback:
			log.trace("bot %s going back" % b.name)
			b.go_back()

		for b in self.bots2remove:
			try:
				self.bots.remove(b)
				log.minor("removed bot %s" % b.name)
			except ValueError:
				pass

		for s in self.shots2remove:
			try:
				self.shots.remove(s)
				log.trace("removed shot from %s at %f, %f" % (s.owner.name, s.pos[0], s.pos[1]))
			except ValueError:
				pass

	def run_scan(self, bot):
		result = []
		for b in self.bots:
			if (b == bot):
				continue
			direction = util.get_direction(bot.pos, b.pos) % 360

			if ( (bot.scanrange[0] <= direction <= bot.scanrange[1]) or (bot.scanrange[0] > bot.scanrange[1] and (direction >= bot.scanrange[0] or direction <= bot.scanrange[1])) ):
				result.append((util.distance(b.pos, bot.pos), (b.name, b.pos, b.direction, b.speed)))

		# sort in base alla distanza (senno' il primo della lista e' svantaggiato)
		result.sort()
		return list(map(lambda x:x[1], result))


	def step(self):
		self.shots2remove = []
		self.bots2goback = []
		self.bots2remove = []

		for b in self.bots:
			b.ai_act()

		self.moveshots()

		self.movebots()

		self.check_collision()

		self.reactions()

		for b in self.bots:
			b.run_scanner()

	def dump(self):
		for b in self.bots:
			log.trace("Bot %s at %f, %f" % (b.name, b.pos[0], b.pos[1]))

		for s in self.shots:
			log.trace("Shot from %s at %f, %f" % (s.owner.name, s.pos[0], s.pos[1]))

	def is_over(self):
		if len(self.bots) == 0:
			return True
		if len(self.bots) == 1:
			for s in self.shots:
				if s.owner != self.bots[0]:
					return False
			return True
		return False

	def dump_winners(self):
		if len(self.bots) == 0:
			log.major("The result is tied (no bots remaining)")
			return []
		elif len(self.bots) == 1:
			log.major("Winner is %s" % self.bots[0].name)
			return [self.bots[0].name]
		else:
			bl = ""
			r = []
			for b in self.bots:
				bl = "%s %s" % (bl, b.name)
				r.append(b.name)
			log.major("Time over... bots remaining:%s" % bl)
			return r


