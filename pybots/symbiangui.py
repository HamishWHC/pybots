#!/usr/bin/env python

import e32
import appuifw
from graphics import *
import time

from pybots import vars


class gui:
	def __init__(self):
		self.img = None
		self.scale = 1
		self.last_redraw = time.time()

	def map(self, x):
		return x * self.scale

	def circle(self, pos, radius, color=0xffffff):
		x = self.map(pos[0])
		y = self.map(pos[1])
		r = self.map(2 * radius)
		self.img.point((x, y), color, width=r)

	def cross(self, pos, radius, color=0xffffff):
		x = self.map(pos[0])
		y = self.map(pos[1])
		r = self.map(radius)
		self.img.line((x-r, y-r, x+r, y+r), color)
		self.img.line((x-r, y+r, x+r, y-r), color)

	def refresh(self):
		self.img.clear(0)

		for b in self.arena.bots:
			self.circle(b.pos, b.size, b.color)

		for s in self.arena.shots:
			self.cross(s.pos, 0.5 / self.scale * s.power, 0xff0000)

	def redraw(self, rect):
		try:
			self.canvas.blit(self.img)
		except:
			pass

	def redrawgui(self):
		self.refresh()
		self.redraw(())

		now = time.time()
		sleep_time = (1.0 / vars.GUI_FPS) - (now - self.last_redraw)
		self.last_redraw = now

		if sleep_time > 0:
			e32.ao_sleep(sleep_time)
		else:
			e32.ao_yield()

	def startgui(self, ar, callback):
		self.arena = ar

		appuifw.app.screen = 'full'
		appuifw.app.body = self.canvas = appuifw.Canvas(redraw_callback=self.redraw)
		self.img = Image.new(self.canvas.size)

		(w, h) = self.canvas.size
		sx = (1.0 * w) / self.arena.width
		sy = (1.0 * h) / self.arena.height
		if (sx < sy):
			self.scale = sx
		else:
			self.scale = sy

		self.last_redraw = time.time()
		while callback():
			self.redrawgui()

