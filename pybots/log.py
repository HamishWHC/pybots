#!/usr/bin/env python

import os
import sys

from . import vars

header = ""

logfile = os.path.join(os.path.dirname(sys.argv[0]), vars.LOGFILE)


def init() -> None:
    global logfile
    try:
        open(logfile, "w").close()
    except IOError as e:
        print(e)


def set_header(hdr) -> None:
    global header
    header = hdr


def write_log(msg: str, level: int = 0) -> None:
    global logfile
    if vars.OUT_VERBOSITY > level:
        print(msg)

    if vars.FILE_VERBOSITY > level:
        try:
            fp = open(logfile, "a")
            fp.write("%s\n" % msg)
            fp.close()
        except IOError as e:
            print(e)


def major(msg: str) -> None:
    write_log("%s%s" % (header, msg), 0)


def minor(msg: str) -> None:
    write_log("%s%s" % (header, msg), 1)


def trace(msg: str) -> None:
    write_log("%s%s" % (header, msg), 2)


init()
