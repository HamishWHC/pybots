#!/usr/bin/env python
from __future__ import annotations

import math
from typing import Tuple, List, TYPE_CHECKING, Optional

from . import log, vars, util
from .mover import Mover
from .shot import Shot

if TYPE_CHECKING:
    from .types import Position, Colour, ShotRequest, ScanResult
    from .arena import Arena
    from .bot_implementation import BotImplementation


class Bot(Mover):
    def __init__(self, name: str, pos: Position, arena: Optional[Arena], impl: BotImplementation,
                 colour: Colour = (0xff, 0xff, 0xff)) -> None:
        super().__init__(pos, 0, 0)

        self.colour: Colour = colour

        self.impl: BotImplementation = impl
        self.arena: Optional[Arena] = arena

        self.damage: int = 0

        self.name: str = name

        self.valid: bool = True

        try:
            self.size: int = impl.size
            self.armour: int = impl.armour
            self.maxdamage: int = impl.maxdamage
            self.maxspeed: int = impl.maxspeed
            self.shotpower: int = impl.shotpower
            self.shotspeed: int = impl.shotspeed
            self.scanradius: int = impl.scanradius

            self.check_valid()
        except Exception as e:
            log.major("Bot " + self.name + " caused exception when setting bot stats: " + str(e))
            self.valid = False

        try:
            data = {
                'ARENA_W': self.arena.width,
                'ARENA_H': self.arena.height,
                'ARENA_WALL_DMG': self.arena.wall_damage,
                'ROUND_DURATION': vars.ROUND_DURATION
            }
            self.impl.set_arena_data(data)
        except Exception as e:
            log.major("Bot " + self.name + " caused exception in set_arena_data(): " + str(e))

        self.scan_result: List[ScanResult] = []
        self.scan_range: Tuple[int, int] = (0, 0)  # from-to degrees

    def check_valid(self) -> bool:
        # size must be 5 - 15
        # armour must be 0-3
        # maxdamage must be 10 - 15
        # maxspeed must be 1 - 5
        # shotpower must be 1 - 5
        # shotspeed must be 3 - 10
        # scanradius must be 1 - 9
        if not (5 <= self.size <= 15):
            self.valid = False
        elif not (0 <= self.armour <= 3):
            self.valid = False
        elif not (10 <= self.maxdamage <= 15):
            self.valid = False
        elif not (1 <= self.maxspeed <= 5):
            self.valid = False
        elif not (1 <= self.shotpower <= 5):
            self.valid = False
        elif not (3 <= self.shotspeed <= 10):
            self.valid = False
        elif not (1 <= self.scanradius <= 9):
            self.valid = False
        return self.valid

    def calc_cost(self) -> int:
        cost = 0
        cost += 15 - self.size
        cost += self.armour * 6
        cost += self.maxdamage - 10
        cost += (self.maxspeed - 1) * 2
        cost += (self.shotpower - 1) * 4
        cost += (self.shotspeed - 3) * 2
        cost += self.scanradius - 1
        return cost

    def shoot(self, direction: float, speed: float, power: float) -> None:
        if speed <= 0.1:
            speed = 0.1

        if speed > self.shotspeed:
            speed = self.shotspeed

        if power < 0:
            power = 0

        if power > self.shotpower:
            power = self.shotpower

        s = Shot(self.position, direction, speed, power, self)
        self.arena.add_shot(s)

    def set_dir(self, direction: float) -> None:
        self.direction: float = direction

    def set_speed(self, speed: float) -> None:
        if speed < 0:
            speed = 0

        if speed > self.maxspeed:
            speed = self.maxspeed

        self.speed: float = speed

    def set_scan(self, direction: float) -> None:
        direction = direction % 360
        self.scan_range = (direction - 10 * self.scanradius, direction + 10 * self.scanradius)

    def die(self) -> None:
        log.minor("%s dying" % self.name)
        self.arena.remove_bot(self)

    def hit(self, power: int) -> None:
        power -= self.armour

        if power < 0:
            power = 0

        self.damage += power

        log.minor("%s hit damage %d - total damage %d" % (self.name, power, self.damage))

        if self.damage >= self.maxdamage:
            self.die()

    def collide(self, pos: Position, size: int = 0):
        return util.get_distance_between_points(pos, self.position) < (self.size + size)

    def ai_act(self) -> None:
        try:
            direction: int
            speed: int
            scanner: int
            shots: List[ShotRequest]
            direction, speed, scanner, shots = self.impl.act((self.name, self.position, self.damage, self.scan_result))

            self.set_dir(math.radians(direction))
            self.set_speed(speed)
            self.set_scan(scanner)

            total_shot = 0
            for s in shots:
                if (total_shot + s[2]) > self.shotpower:
                    # FIXME: This attempts to write to a tuple whenever a Bot Implementation goes over its shotpower.
                    #  It gets caught by the try-except, but that is luck, not intentional.
                    s[2] = self.shotpower - total_shot
                self.shoot(math.radians(s[0]), s[1], s[2])
                total_shot += s[2]
                if total_shot >= self.shotpower:
                    break
        except Exception as e:
            log.minor("%s - error %s" % (self.name, e))
            self.hit(vars.EXCEPTION_COST)

    def run_scanner(self) -> None:
        self.scan_result = self.arena.run_scan(self)
