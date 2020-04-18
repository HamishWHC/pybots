#!/usr/bin/env python
from __future__ import annotations

import random
from typing import List, TYPE_CHECKING

from . import log, util

if TYPE_CHECKING:
    from .bot import Bot
    from .shot import Shot
    from .types import Position, ScanResult

random.seed()


class Arena:
    def __init__(self, width: int = 400, height: int = 300, wall_damage: int = 0) -> None:
        self.bots: List[Bot] = []
        self.shots: List[Shot] = []

        self.width: int = width
        self.height: int = height
        self.wall_damage: int = wall_damage

        self.shots_to_remove: List[Shot] = []
        self.bots_to_revert: List[Bot] = []
        self.bots_to_remove: List[Bot] = []

    def check_random_pos(self, pos: Position, radius: int) -> bool:
        if not (self.inside(pos, radius)):
            return False
        else:
            for b in self.bots:
                if b.collide(pos, radius):
                    return False
        return True

    def get_random_pos(self, radius: int) -> Position:
        redo = True
        tries = 0
        while redo and tries < 100:
            redo = False
            x = radius + random.random() * (self.width - 2 * radius)
            y = radius + random.random() * (self.height - 2 * radius)
            pos = (x, y)
            if not (self.check_random_pos(pos, radius)):
                redo = True
            tries += 1

        if redo:
            raise Exception("Arena is too small")

        return pos  # FIXME: Write a better method entirely.

    def add_bot(self, bot: Bot, recalc_pos: bool = True) -> None:
        if recalc_pos:
            bot.position = self.get_random_pos(bot.size)
        self.bots.append(bot)

    def add_shot(self, shot: Shot) -> None:
        self.shots.append(shot)

    def remove_bot(self, bot: Bot) -> None:
        self.bots_to_remove.append(bot)

    def remove_shot(self, shot: Shot) -> None:
        self.shots_to_remove.append(shot)

    def inside(self, pos: Position, size: int = 0) -> bool:
        return (pos[0] >= size) and (pos[1] >= size) and (pos[0] <= self.width - size) and (
                pos[1] <= self.height - size)

    def move_shots(self) -> None:
        for s in self.shots:
            s.move()
            if not (self.inside(s.position)):
                self.remove_shot(s)

    def move_bots(self) -> None:
        for b in self.bots:
            b.move()
            if not (self.inside(b.position, b.size)):
                log.minor("bot %s hits arena wall" % b.name)
                b.hit(self.wall_damage)
                self.bots_to_revert.append(b)

    def check_collision(self) -> None:
        for s in self.shots:
            for b in self.bots:
                if s.owner == b:
                    continue

                if b.collide(s.position, 0):
                    log.minor("%s hit %s" % (s.owner.name, b.name))
                    b.hit(s.power)
                    self.shots_to_remove.append(s)

        for b1 in self.bots:
            for b2 in self.bots:
                if b1 == b2:
                    continue

                if b1.collide(b2.position, b2.size):
                    log.minor("%s collided with %s" % (b1.name, b2.name))
                    b2.hit(b1.armour)
                    self.bots_to_revert.append(b1)
                    self.bots_to_revert.append(b2)

    def reactions(self) -> None:
        # TODO: Move into the remove_bot, remove_shot and check_collision methods. No need to re-iterate.
        for b in self.bots_to_revert:
            log.trace("bot %s going back" % b.name)
            b.revert_position()

        for b in self.bots_to_remove:
            try:
                self.bots.remove(b)
                log.minor("removed bot %s" % b.name)
            except ValueError:
                pass

        for s in self.shots_to_remove:
            try:
                self.shots.remove(s)
                log.trace("removed shot from %s at %f, %f" % (s.owner.name, s.position[0], s.position[1]))
            except ValueError:
                pass

    def run_scan(self, bot: Bot) -> List[ScanResult]:
        results = []
        for b in self.bots:
            if b == bot:
                continue
            direction = util.get_direction(bot.position, b.position) % 360

            if ((bot.scan_range[0] <= direction <= bot.scan_range[1]) or (bot.scan_range[0] > bot.scan_range[1] and (
                    direction >= bot.scan_range[0] or direction <= bot.scan_range[1]))):
                results.append((util.get_distance_between_points(b.position, bot.position),
                                (b.name, b.position, b.direction, b.speed)))

        # sort by distance to scanned bot.
        results.sort()
        return [result[1] for result in results]

    def step(self) -> None:
        self.shots_to_remove = []
        self.bots_to_revert = []
        self.bots_to_remove = []

        for b in self.bots:
            b.ai_act()

        self.move_shots()

        self.move_bots()

        self.check_collision()

        self.reactions()

        for b in self.bots:
            b.run_scanner()

    def dump(self) -> None:
        # TODO: Move into the movement methods instead of re-iterating.
        for b in self.bots:
            log.trace("Bot %s at %f, %f" % (b.name, b.position[0], b.position[1]))

        for s in self.shots:
            log.trace("Shot from %s at %f, %f" % (s.owner.name, s.position[0], s.position[1]))

    def is_over(self) -> bool:
        if len(self.bots) == 0:
            return True
        if len(self.bots) == 1:
            for s in self.shots:
                if s.owner != self.bots[0]:
                    return False
            return True
        return False

    def dump_winners(self) -> List[str]:
        if len(self.bots) == 0:
            log.major("The result is tied (no bots remaining)")
            return []
        elif len(self.bots) == 1:
            log.major("Winner is %s" % self.bots[0].name)
            return [self.bots[0].name]
        else:
            bl = ""
            r = []
            for b in self.bots:
                bl = "%s %s" % (bl, b.name)
                r.append(b.name)
            log.major("Time over... bots remaining:%s" % bl)
            return r
