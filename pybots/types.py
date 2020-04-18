from typing import Union, Tuple

Colour = Tuple[Union[int, hex], Union[int, hex], Union[int, hex]]  # 3 integers (0 to 255) or hex values (0x00 to 0xff)
Position = Tuple[float, float]  # x, y
ScanResult = Tuple[str, Position, float, float]  # name, position, direction, speed
ShotRequest = Tuple[int, int, int]  # direction, speed, power
ArenaData = Tuple[int, int, int]  # width, height, wall damage
BotData = Tuple[str, "BotImplementation", Colour]
