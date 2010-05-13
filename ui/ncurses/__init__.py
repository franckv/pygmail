# -*- coding: utf-8 -*-   

import curses
import locale
import logging

import common
import log
from widget import Screen
from commandhandler import CommandHandler

#locale.setlocale(locale.LC_ALL, '')

def main(stdscr):
    log.init(logging.DEBUG, '/tmp/pygmail.log')
    log.debug('Start')

    screen = Screen(stdscr)

    screen.set_encoding(locale.getpreferredencoding())

    screen.set_title('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.set_status('Standby ready')

    screen.refresh()

    handler = CommandHandler(screen)
    handler.handle()

def run(args = None):
    curses.wrapper(main)
    log.debug('Stop')

if __name__ == '__main__':
    run()

