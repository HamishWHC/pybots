#!/usr/bin/env python

"""

Randmover
pybot by Alessandro Pira

moves and scans randomly

"""

import random
from pybots import util


class Bot:
    size = 10
    armour = 1
    maxdamage = 10
    maxspeed = 1
    shotpower = 4
    shotspeed = 5
    # * 10 in degrees
    scanradius = 4

    def __init__(self):
        self.direction = random.randint(0, 359)

    def act(self, data):
        (name, pos, dmg, scanresult) = data
        if random.randint(0, 5) == 0:
            self.direction = random.randint(0, 359)
        scan = random.randint(0, 359)
        shot = []
        if len(scanresult) > 0:
            sdir = util.get_direction(pos, scanresult[0][1])
            shot.append((sdir, self.shotspeed, self.shotpower))

        return (self.direction, self.maxspeed, scan, shot)
