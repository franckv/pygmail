import os, sys
from optparse import OptionParser

import commands

def help(cmd = None):
    if not cmd:
        print 'Usage: %s COMMAND [ARGS]' % sys.argv[0]
    else:
        print 'Usage: %s %s [ARGS]' % (sys.argv[0], sys.argv[1])

if __name__ == '__main__':
    parser = OptionParser()

    (options, args) = parser.parse_args()

    if len(args) == 0:
        help()
    else:
        cmd = args[0]

        if not cmd in commands.list:
            help()
        else:
            nargs = int(commands.list[cmd]['args'])

            if nargs != len(args) - 1:
                help(cmd)
            else:
                commands.list[cmd]['exec'](*args[1:])

