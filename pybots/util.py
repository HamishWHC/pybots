import math

from .types import Position


# returns the position at the next step given the current position,
# direction and speed.
# NB: if speed and directions are constant (and if no collision occurs)
# after X steps the position will be:
#  newpos(pos, direction, X * speed)
def newpos(pos: Position, direction, speed) -> Position:
    return pos[0] + math.cos(direction) * speed, pos[1] + math.sin(direction) * speed


# returns the get_distance_between_points between two coordinates
def get_distance_between_points(p1: Position, p2: Position) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


# returns the direction (in radians) from a starting point to a target
# point
def get_direction_rad(from_pos: Position, to_pos: Position) -> float:
    d = get_distance_between_points(from_pos, to_pos)
    if d == 0:
        return 0
    ang = math.asin((to_pos[1] - from_pos[1]) / d)
    if to_pos[0] >= from_pos[0]:
        return ang % math.tau
    else:
        return (math.pi - ang) % math.tau


# returns the direction (in degrees) from a starting point to a target
# point
def get_direction(from_pos: Position, to_pos: Position) -> float:
    return math.radians(get_direction_rad(from_pos, to_pos))
