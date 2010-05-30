import os, sys
from optparse import OptionParser
import logging

import log
import command
import ui.ncurses, ui.gtkui

if __name__ == '__main__':
    log.init(logging.WARN, '/tmp/pygmail.log')
    log.debug('Start')

    usage = 'Usage: %prog COMMAND [ARGS]'
    parser = OptionParser(usage)
    parser.add_option('--ui', dest='ui', default='console', help='interface: curses, gtk or console (default)')

    (options, args) = parser.parse_args()

    if options.ui == 'curses':
        ui.ncurses.run()
    elif options.ui == 'gtk':
        ui.gtkui.run()
    else:
        if len(args) == 0:
            parser.error('missing command')

        cmd = args[0]

        if not cmd in command.list:
            parser.error('invalid command')
        else:
            nargs = int(command.list[cmd]['args'])

            if nargs != len(args) - 1:
                parser.error('wrong number of arguments (expected %i)' % nargs)
            else:
                command.list[cmd]['exec'](*args[1:])


    log.debug('Stop')
