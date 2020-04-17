#!/usr/bin/env python

from . import log, shot, vars, util, mover


class bot (mover.mover):
	def __init__(self, name, pos, arena, impl, color=(0xff,0xff,0xff)):
		mover.mover.__init__(self, pos, 0, 0)

		self.color = color

		self.impl = impl
		self.arena = arena

		self.damage = 0

		self.name = name

		try:
			# size must be 5 - 15
			# armour must be 0-3
			# maxdamage must be 10 - 15
			# maxspeed must be 1 - 5
			# shotpower must be 1 - 5
			# shotspeed must be 3 - 10
			# scanradius must be 1 - 9
			self.size = impl.size
			self.armour = impl.armour
			self.maxdamage = impl.maxdamage
			self.maxspeed = impl.maxspeed
			self.shotpower = impl.shotpower
			self.shotspeed = impl.shotspeed
			self.scanradius = impl.scanradius
		except:
			self.size = -1 # Bot is not valid

		try:
			data = {}
			data['ARENA_W'] = self.arena.width
			data['ARENA_H'] = self.arena.height
			data['ARENA_WALL_DMG'] = self.arena.wallpower
			data['ROUND_DURATION'] = vars.ROUND_DURATION
			self.impl.set_arena_data(data)
		except:
			pass

		self.scanresult = []
		self.scanrange = (0, 0) # from-to degrees

	def check_valid(self):
		if not(5 <= self.size <= 15):
			return False
		if not(0 <= self.armour <= 3):
			return False
		if not(10 <= self.maxdamage <= 15):
			return False
		if not(1 <= self.maxspeed <= 5):
			return False
		if not(1 <= self.shotpower <= 5):
			return False
		if not(3 <= self.shotspeed <= 10):
			return False
		if not(1 <= self.scanradius <= 9):
			return False
		return True

	def calc_cost(self):
		cost = 0
		cost += 15 - self.size
		cost += self.armour * 6
		cost += self.maxdamage - 10
		cost += (self.maxspeed - 1) * 2
		cost += (self.shotpower - 1) * 4
		cost += (self.shotspeed - 3) * 2
		cost += self.scanradius - 1
		return cost

	def shoot(self, direction, speed, power):
		if speed <= 0.1:
			speed = 0.1

		if speed > self.shotspeed:
			speed = self.shotspeed

		if power < 0:
			power = 0

		if power > self.shotpower:
			power = self.shotpower

		s = shot.shot(self.pos, direction, speed, power, self)
		self.arena.addshot(s)

	def setdir(self, direction):
		self.direction = direction

	def setspeed(self, speed):
		if (speed < 0):
			speed = 0

		if (speed > self.maxspeed):
			speed = self.maxspeed

		self.speed = speed

	def setscan(self, direction):
		direction = direction % 360
		self.scanrange = (direction - 10*self.scanradius, direction + 10*self.scanradius)

	def die(self):
		log.minor("%s dying" % self.name)
		self.arena.removebot(self)

	def hit(self, power):
		power -= self.armour

		if (power < 0):
			power = 0

		self.damage += power

		log.minor("%s hit damage %d - total damage %d" % (self.name, power, self.damage))

		if (self.damage >= self.maxdamage):
			self.die()

	def collide(self, pos, size=0):
		return util.distance(pos, self.pos) < (self.size + size)

	def ai_act(self):
		try:
			(direction, speed, scanner, shots) = self.impl.act((self.name, self.pos, self.damage, self.scanresult))

			self.setdir(util.deg2rad(direction))
			self.setspeed(speed)
			self.setscan(scanner)

			totalshot = 0
			for s in shots:
				if (totalshot + s[2]) > self.shotpower:
					s[2] = self.shotpower - totalshot
				self.shoot(util.deg2rad(s[0]), s[1], s[2])
				totalshot += s[2]
				if totalshot >= self.shotpower:
					break
		except Exception as e:
			log.minor("%s - error %s" % (self.name, e))
			self.hit(vars.EXCEPTION_COST)
			return

	def run_scanner(self):
		self.scanresult = self.arena.run_scan(self)

