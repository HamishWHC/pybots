#!/usr/bin/env python

"""

Alex I
pybot by Alessandro Pira

Features:
- runs around arena corners, changing corner when hit
- when a pybot is scanned the following scan tries to follow the same bot
- checks for the direction and speed of a target trying to calculate shots
  as if the target runs straight and at the same speed

"""

import random
from pybots import util
from pybots.bot_implementation import BotImplementation


class Bot(BotImplementation):
    size = 8
    armour = 1
    maxdamage = 10
    maxspeed = 3
    shotpower = 4
    shotspeed = 3
    # * 10 in degrees
    scanradius = 2

    def __init__(self):
        self.lastdmg = 0
        self.scannedbot = None
        self.corners = [
            (self.size, self.size),
            (self.size, self.size),
            (self.size, self.size),
            (self.size, self.size)
        ]
        self.current_corner = -1

    def set_arena_data(self, data):
        self.arenaw = data['ARENA_W']
        self.arenah = data['ARENA_H']
        self.walldmg = data['ARENA_WALL_DMG']
        self.round_duration = data['ROUND_DURATION']
        self.corners = [
            (self.size, self.size),
            (self.size, self.arenah - self.size),
            (self.arenaw - self.size, self.arenah - self.size),
            (self.arenaw - self.size, self.size)
        ]

    def act(self, data):
        (name, pos, dmg, scanresult) = data

        scan = random.randint(0, 359)
        shot = []

        if (self.current_corner < 0):
            # At start run to the closest corner
            mindist = util.get_distance_between_points(pos, self.corners[0])
            mindistidx = 0
            for i in range(1, len(self.corners)):
                d = util.get_distance_between_points(pos, self.corners[i])
                if (d < mindist):
                    mindist = d
                    mindistidx = i
            self.current_corner = mindistidx
        elif (dmg > self.lastdmg):
            # When hit change corner
            self.current_corner += 1
            if (self.current_corner >= len(self.corners)):
                self.current_corner = 0

        corner = self.corners[self.current_corner]
        corner_dist = util.get_distance_between_points(pos, corner)
        if (corner_dist <= self.maxspeed * 2):
            direction = 0
            speed = 0
            # If we are in a corner, reduce scanning range
            if (self.current_corner == 0):
                scan = random.randint(-5, 95)
            elif (self.current_corner == 1):
                scan = random.randint(265, 365)
            elif (self.current_corner == 2):
                scan = random.randint(175, 275)
            elif (self.current_corner == 3):
                scan = random.randint(85, 185)
        else:
            direction = util.get_direction(pos, corner)
            speed = self.maxspeed

        self.lastdmg = dmg

        if len(scanresult) > 0:
            if ((self.scannedbot) and (self.scannedbot[0] == scanresult[0][0])):
                bspeed = util.get_distance_between_points(scanresult[0][1], self.scannedbot[1])
            else:
                bspeed = None
            self.scannedbot = scanresult[0]
            if (bspeed != None):
                self.scannedbot = self.scannedbot[:-1] + (bspeed,)
        else:
            self.scannedbot = None

        if self.scannedbot:
            (bot_name, bot_pos, bot_dir, bot_speed) = self.scannedbot

            # Track bot with scanner
            scanpoint = util.newpos(bot_pos, bot_dir, bot_speed)
            scan = util.get_direction(pos, scanpoint)

            distance = util.get_distance_between_points(pos, bot_pos)

            # Shooting management
            target = bot_pos
            for shot_steps in range(0, 1000):
                distance = util.get_distance_between_points(pos, target)
                if (distance <= self.shotspeed * shot_steps):
                    # Impact point found: shoot
                    shot_dir = util.get_direction(pos, target)
                    shot_speed = distance / shot_steps
                    shot.append((shot_dir, shot_speed, self.shotpower))
                    break
                target = util.newpos(target, bot_dir, bot_speed)

                # Target outside of arena, cannot hit
                if ((target[0] < 0) or (target[0] > self.arenaw) or (target[1] < 0) or (target[1] > self.arenah)):
                    break

        return (direction, speed, scan, shot)
