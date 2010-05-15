# -*- coding: utf-8 -*-   

import curses
import locale
import logging

import common
import log
from window import Window
from commandhandler import CommandHandler

def main(stdscr):
    log.init(logging.DEBUG, '/tmp/pygmail.log')
    log.debug('Start')

    screen = Window(stdscr)

    screen.set_title('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.set_status('Standby ready')

    screen.refresh()

    handler = CommandHandler(screen)
    handler.handle()

def run(args = None):
    curses.wrapper(main)
    log.debug('Stop')

