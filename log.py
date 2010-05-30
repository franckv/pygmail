import logging

import common

def init(level, filename):
    logging.basicConfig(
        level = level,
        format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
        datefmt="%H:%M:%S",
        filename = filename,
        filemode = 'w'
    )

debug = logging.debug
warn = logging.warn

logger = logging.getLogger(common.PROGNAME)
