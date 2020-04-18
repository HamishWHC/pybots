#!/usr/bin/env python

"""

Rammer
pybot by Alessandro Pira

Uses speed and armor and tries to ram other pybots

"""

import random
from pybots import util


class Bot:
    size = 15
    armour = 3
    maxdamage = 10
    maxspeed = 5
    shotpower = 1
    shotspeed = 4
    # * 10 in degrees
    scanradius = 3

    def __init__(self):
        self.scanner = random.randint(0, 359)
        self.scandir = random.randrange(-20, 40, 40)
        self.lastscansuccess = False
        self.nextscan = None
        self.lastdir = random.randint(0, 359)

    def set_arena_data(self, data):
        self.arenaw = data['ARENA_W']
        self.arenah = data['ARENA_H']

    def act(self, data):
        (name, pos, damage, scanresult) = data

        if len(scanresult) == 0:
            if self.nextscan:
                self.scanner = self.nextscan
                self.nextscan = None
            else:
                if self.lastscansuccess:
                    # if we lost sight of a pybot try scanning around the last
                    # scan direction, left and right
                    self.scandir = random.randrange(-20, 40, 40)
                    self.nextscan = self.scanner + self.scandir
                    self.scanner -= self.scandir
                else:
                    self.scanner += self.scandir
            self.lastscansuccess = False
            direction = self.lastdir
        else:
            self.lastscansuccess = True
            direction = util.get_direction(pos, scanresult[0][1])
            self.lastdir = direction
            self.scanner = direction

        return (direction, self.maxspeed, self.scanner, [(direction, self.shotspeed, self.shotpower)])
