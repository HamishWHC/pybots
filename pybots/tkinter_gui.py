#!/usr/bin/env python

import time
from tkinter import *
from typing import Callable

from pybots import vars
from .arena import Arena
from .types import Colour, Position


def map_float(x: float) -> float:
    return x * vars.GUI_SCALE


def map_color(col: Colour) -> str:
    return "#%.2x%.2x%.2x" % col


class GUI:
    def __init__(self) -> None:
        self.root = None
        self.last_redraw = time.time()
        self.arena = None
        self.callback = None
        self.canvas = None

    def circle(self, pos: Position, radius: int, colour: Colour = (255, 255, 255)) -> None:
        x = map_float(pos[0])
        y = map_float(pos[1])
        r = map_float(radius)
        colour = map_color(colour)
        self.canvas.create_arc(x - r, y - r, x + r, y + r, fill=colour, style=CHORD, start=0, extent=359, width=0)

    def cross(self, pos: Position, radius: int, colour: Colour = (255, 255, 255)) -> None:
        x = map_float(pos[0])
        y = map_float(pos[1])
        r = map_float(radius)
        colour = map_color(colour)
        self.canvas.create_line(x - r, y - r, x + r, y + r, fill=colour)
        self.canvas.create_line(x - r, y + r, x + r, y - r, fill=colour)

    def redraw(self) -> None:
        try:
            for i in self.canvas.find_all():
                self.canvas.delete(i)

            for b in self.arena.bots:
                self.circle(b.position, b.size, b.colour)

            for s in self.arena.shots:
                self.cross(s.position, 0.5 / vars.GUI_SCALE * s.power, (0xff, 0, 0))
        except TclError:
            pass

    def redraw_gui(self) -> None:
        if self.callback and self.callback():
            self.redraw()

            now = time.time()
            sleep_time = (1.0 / vars.GUI_FPS) - (now - self.last_redraw)
            if sleep_time <= 0:
                sleep_time = 0.001
            self.last_redraw = now
            self.root.after(int(sleep_time * 1000), self.redraw_gui)
        else:
            self.root.quit()

    def start_gui(self, ar: Arena, callback: Callable) -> None:
        self.arena = ar
        self.callback = callback

        self.root = Tk()
        self.root.title('PyBots')
        frame = Frame(self.root)
        frame.pack()

        self.canvas = Canvas(frame, height=map_float(self.arena.height), width=map_float(self.arena.width),
                             bg=map_color((0, 0, 0)))
        self.canvas.pack()

        self.last_redraw = time.time()
        self.root.after(1, self.redraw_gui)
        self.root.mainloop()

        try:
            self.root.destroy()
        except TclError:
            pass
