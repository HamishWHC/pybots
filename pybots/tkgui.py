#!/usr/bin/env python

from tkinter import *
import time

from pybots import vars


class gui:
	def __init__(self):
		self.root = None
		self.last_redraw = time.time()

	def map(self, x):
		return x * vars.GUI_SCALE

	def mapcolor(self, col):
		return "#%.2x%.2x%.2x" % col

	def circle(self, pos, radius, color=(0xff,0xff,0xff)):
		x = self.map(pos[0])
		y = self.map(pos[1])
		r = self.map(radius)
		color = self.mapcolor(color)
		self.canvas.create_arc(x-r, y-r, x+r, y+r, fill=color, style=CHORD, start=0, extent=359, width=0)

	def cross(self, pos, radius, color=(0xff,0xff,0xff)):
		x = self.map(pos[0])
		y = self.map(pos[1])
		r = self.map(radius)
		color = self.mapcolor(color)
		self.canvas.create_line(x-r, y-r, x+r, y+r, fill=color)
		self.canvas.create_line(x-r, y+r, x+r, y-r, fill=color)

	def redraw(self):
		try:
			for i in self.canvas.find_all():
				self.canvas.delete(i)

			for b in self.arena.bots:
				self.circle(b.pos, b.size, b.color)

			for s in self.arena.shots:
				self.cross(s.pos, 0.5 / vars.GUI_SCALE * s.power, (0xff, 0, 0))
		except TclError:
			pass

	def redrawgui(self):
		if (self.callback()):
			self.redraw()

			now = time.time()
			sleep_time = (1.0 / vars.GUI_FPS) - (now - self.last_redraw)
			if (sleep_time <= 0):
				sleep_time = 0.001
			self.last_redraw = now
			self.root.after(int(sleep_time * 1000), self.redrawgui)
		else:
			self.root.quit()

	def startgui(self, ar, callback):
		self.arena = ar
		self.callback = callback

		self.root = Tk()
		self.root.title('PyBots')
		frame = Frame(self.root)
		frame.pack()

		self.canvas = Canvas(frame,height=self.map(self.arena.height),width=self.map(self.arena.width),bg=self.mapcolor((0,0,0)))
		self.canvas.pack()

		self.last_redraw = time.time()
		self.root.after(1, self.redrawgui)
		self.root.mainloop()

		try:
			self.root.destroy()
		except TclError:
			pass

