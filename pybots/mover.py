#!/usr/bin/env python

from . import util
from .types import Position


class Mover:
    def __init__(self, pos: Position, direction: float, speed: int) -> None:
        self.previous_position: Position = pos
        self.position: Position = pos
        self.direction: float = direction
        self.speed: float = speed

    def move(self) -> None:
        self.previous_position = self.position
        self.position = util.newpos(self.position, self.direction, self.speed)

    def revert_position(self) -> None:
        self.position = self.previous_position
