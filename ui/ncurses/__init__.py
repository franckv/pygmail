# -*- coding: utf-8 -*-   

import curses
import locale

import common
from screen import Screen

locale.setlocale(locale.LC_ALL, '')

def main(stdscr):
    screen = Screen(stdscr)

    screen.encoding = locale.getpreferredencoding()

    screen.title.set_text('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.status.set_text('Standby ready')

    screen.refresh()

    while True:
        c = screen.command.get_char()

        if c is None:
            continue

        (y, x) = screen.get_pos()
        screen.status.set_text('(%i, %i) : <%s>' % (y, x, c.strip()))

        if c == '<KEY_LEFT>':
            (y, x) = screen.get_pos()
            screen.move(y, x-1)
        elif c == '<KEY_RIGHT>':
            (y, x) = screen.get_pos()
            screen.move(y, x+1)
        elif c == '<KEY_DOWN>':
            screen.win.scroll(1)
            screen.refresh()
        elif c == '<KEY_UP>':
            screen.win.scroll(-1)
            screen.refresh()
        elif c == '<KEY_RESIZE>':
            screen.resize()
        elif c == ':':
            screen.read_command()
        elif c == '<KEY_ENTER>' or c == '\n':
            (y, x) = screen.get_pos()
            (maxy, maxx) = screen.win.getmaxyx()
            if y < maxy - 3:
                screen.move(y+1, 0)
        else:
            screen.main.write(c)

def run(args = None):
    curses.wrapper(main)

if __name__ == '__main__':
    run()

