#!/usr/bin/env python

from typing import List, Optional

from . import arena, log, vars, bot, bot_loader, tkinter_gui
from .arena import Arena
from .types import ArenaData, BotData

ar: Optional[Arena] = None
bots: Optional[List[BotData]] = None
arena_list: List[ArenaData] = []
gui: Optional[tkinter_gui.GUI] = None
step: int = 0


def begin_round(ar_data: ArenaData = None) -> None:
    global bots, ar

    if bots is None:
        begin_tournament()

    try:
        if ar_data is None:
            ar_data = arena_list.pop()
        ar = arena.Arena(ar_data[0], ar_data[1], ar_data[2])
    except IndexError:
        log.major("Running in default arena")
        ar = arena.Arena()

    for (name, ai, color) in bots:
        b = bot.Bot(name, (0, 0), ar, ai, color)
        if not b.check_valid():
            log.major("Bot %s is disqualified (invalid hardware)" % name)
            continue
        if b.calc_cost() > vars.MAX_BOT_COST:
            log.major("Bot %s is disqualified (hardware too expensive)" % name)
            continue
        ar.add_bot(b)


def run_step() -> bool:
    global ar, step
    log.set_header("%4d - " % step)
    ar.step()
    ar.dump()
    step += 1
    log.set_header("")
    return not (ar.is_over()) and (step < vars.ROUND_DURATION)


def run() -> None:
    while run_step():
        # FIXME: This is the dumbest (and yet most genius) thing I've ever seen.
        #  Should be separated to a check and run_step().
        pass


def run_round() -> List[str]:
    global gui, ar, step

    gui = None

    if vars.GUI_ENABLED:
        gui = tkinter_gui.GUI()

    step = 0

    if gui:
        gui.start_gui(ar, run_step)
    else:
        run()

    return ar.dump_winners()


def begin_tournament(arenas: List[ArenaData] = None, rpa: int = 1) -> None:
    global bots, arena_list

    if arenas is None:
        arenas = []

    bots = bot_loader.load_bots()

    for a in arenas:
        if len(a) == 3:
            for i in range(rpa):
                arena_list.append(a)


def run_tournament() -> List[str]:
    global bots, arena_list

    wins = {}

    while len(arena_list) > 0:
        begin_round()
        w = run_round()
        for bw in w:
            try:
                wins[bw] = wins[bw] + 1
            except KeyError:
                wins[bw] = 1

    log.major("Tournament results:")
    maxwin = 0
    winners = []
    for (bot_name, win) in wins.items():
        log.major("%s -> %d" % (bot_name, win))
        if win > maxwin:
            winners = [bot_name]
        elif win == maxwin:
            winners.append(bot_name)

    return winners
