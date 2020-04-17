#!/usr/bin/env python

from . import mover


class shot (mover.mover):
	def __init__(self, pos, direction, speed, power, bot):
		mover.mover.__init__(self, pos, direction, speed)
		self.owner = bot
		self.power = power


