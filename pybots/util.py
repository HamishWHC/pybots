#!/usr/bin/env python

import math

# radians -> degree conversion
def rad2deg(rad):
	return ((rad / math.pi) * 180.0) % 360

# degree -> radians conversion
def deg2rad(deg):
	deg = deg % 360
	return (deg / 180.0) * math.pi

# returns the position at the next step given the current position,
# direction and speed.
# NB: if speed and directions are constant (and if no collision occurs)
# after X steps the position will be:
#  newpos(pos, direction, X * speed)
def newpos(pos, direction, speed):
	return (pos[0] + math.cos(direction) * speed, pos[1] + math.sin(direction) * speed)

# returns the distance between two coordinates
def distance(p1, p2):
	return math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))

# returns the distance between two coordinates
def distance2(x1, y1, x2, y2):
	return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# returns the direction (in radians) from a starting point to a target
# point
def get_direction_rad(from_pos, to_pos):
	d = distance(from_pos, to_pos)
	if (d == 0):
		return 0
	ang = math.asin((to_pos[1] - from_pos[1]) / d)
	if (to_pos[0] >= from_pos[0]):
		return ang % (2 * math.pi)
	else:
		return (math.pi - ang) % (2 * math.pi)

# returns the direction (in degrees) from a starting point to a target
# point
def get_direction(from_pos, to_pos):
	return rad2deg(get_direction_rad(from_pos, to_pos))

