#!/usr/bin/env python

from pybots import util


class mover:
	def __init__(self, pos, direction, speed):
		self.old_pos = pos
		self.pos = pos
		self.direction = direction
		self.speed = speed

	def move(self):
		self.old_pos = self.pos
		self.pos = util.newpos(self.pos, self.direction, self.speed)

	def go_back(self):
		self.pos = self.old_pos

