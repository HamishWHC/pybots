#!/usr/bin/env python

from . import mover


class Shot(mover.Mover):
    def __init__(self, pos, direction, speed, power, bot):
        super().__init__(pos, direction, speed)
        self.owner = bot
        self.power = power
