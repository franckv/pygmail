import os, sys
from optparse import OptionParser
import logging

import command
import ui.ncurses #, ui.gtkui

if __name__ == '__main__':
    logging.basicConfig(
        level = logging.DEBUG,
        format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
        datefmt="%H:%M:%S",
        filename = '/tmp/pygmail.log',
        filemode = 'w'
    )

    logging.debug('Start')

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


    logging.debug('Stop')
