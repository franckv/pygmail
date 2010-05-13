# -*- coding: utf-8 -*-   

import curses
import locale

import common
from widget import Screen
from commandhandler import CommandHandler

locale.setlocale(locale.LC_ALL, '')

def main(stdscr):
    screen = Screen(stdscr)

    screen.set_encoding(locale.getpreferredencoding())

    screen.title.set_text('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.status.set_text('Standby ready')

    screen.refresh()

    handler = CommandHandler(screen)
    handler.handle()

def run(args = None):
    curses.wrapper(main)

if __name__ == '__main__':
    run()

