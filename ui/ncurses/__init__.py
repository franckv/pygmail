# -*- coding: utf-8 -*-   

import curses
import locale

import common
from ui.ncurses.window import Window

def main(stdscr):
    screen = Window(stdscr)

    screen.set_title('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.set_status('Standby ready')

    screen.refresh()

    screen.run()

def run(args = None):
    curses.wrapper(main)

