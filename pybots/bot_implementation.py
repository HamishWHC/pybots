from abc import ABC, abstractmethod
from typing import Tuple, Dict, List

from .types import Position, ScanResult, ShotRequest


class BotImplementation(ABC):
    # Total bot cost must be <= vars.MAX_BOT_COST and is calculated this way:
    #   every size point less than 15 costs 1 (smaller is more expensive)
    #   every armour point costs 6
    #   every maxdamage point beyond 10 costs 1
    #   every maxspeed point beyond 1 costs 2
    #   every shotpower point beyond 1 costs 4
    #   every shotspeed point beyond 3 costs 2
    #   every scanradius point beyond 1 costs 1

    size: int  # must be 5 - 15
    armour: int  # must be 0 - 3
    maxdamage: int  # must be 10 - 15
    maxspeed: int  # must be 1 - 5
    shotpower: int  # must be 1 - 5
    shotspeed: int  # must be 3 - 10
    scanradius: int  # must be 1 - 9

    # This (if present) will be called once at the beginning of the round
    #  round_params is a dictionary which will contain some round-specific
    #  parameters; actually populated keys are ARENA_W, ARENA_H,
    #  ARENA_WALL_DMG, ROUND_DURATION
    @abstractmethod
    def set_arena_data(self, round_params: Dict[str, int]) -> None:
        pass

    # Return (dir, speed, scan_dir, (shots))
    #  (shots) is a list of (dir, speed, power) tuples
    #  data is (name, pos, damage, scanresult)
    #  scanresult is a list of (name, pos, dir, speed) for all scanned bots
    @abstractmethod
    def act(self, data: Tuple[str, Position, int, List[ScanResult]]) -> Tuple[float, float, float, List[ShotRequest]]:
        pass
