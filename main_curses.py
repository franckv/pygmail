# -*- coding: utf-8 -*-   

import sys
import curses
import curses.ascii
import locale

import common
import commands

class Screen:
    def __init__(self, win):
        self.win = win
        self.set_colors()

    def write_char(self, s, attr = None):
        if attr is None: attr = curses.A_NORMAL
        self.win.addch(s, attr)

    def write_str(self, s, attr = None):
        if attr is None: attr = curses.A_NORMAL
        self.win.addstr(s.encode(self.encoding), attr)

    def get_pos(self):
        return self.win.getyx()

    def get_size(self):
        return self.win.getmaxyx()

    def get_char(self):
        return self.win.getch()

    def move(self, y, x):
        self.win.move(y, x)

    def set_title(self, s):
        (y, x) = self.get_pos()
        self.win.move(0, 0)
        self.write_str(self.pad_string(s), self.get_color('title') | curses.A_BOLD)
        self.win.move(y, x)

    def set_status(self, s):
        (y, x) = self.get_pos()
        (maxy, maxx) = self.win.getmaxyx()
        if maxy < 2: return
        self.win.move(maxy-2, 0)
        self.write_str(self.pad_string(s), self.get_color('status') | curses.A_BOLD)
        self.win.move(y, x)

    def read_command(self):
        (maxy, maxx) = self.win.getmaxyx()
        (posy, posx) = self.get_pos()
        if maxy < 1: return
        self.win.move(maxy-1, 0)

        self.write_str(':')
        cmd = ''

        while(True):
            c = self.get_char()
            if c == curses.KEY_ENTER or c == 10:
                break
            elif c == curses.KEY_LEFT:
                (y, x) = self.get_pos()
                self.move(y, x-1)
            elif c == curses.KEY_RIGHT:
                (y, x) = self.get_pos()
                self.move(y, x+1)
            elif curses.ascii.isprint(c):
                if len(cmd) >= maxx - 2:
                    continue
                cmd += chr(c)
                self.write_char(c)
                self.set_status('%i/%i' % (len(cmd), maxx))

        self.handle_command(cmd)

        self.clear_line()
        self.move(posy, posx)

    def handle_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            sys.exit(0)

    def clear_line(self):
        (y, x) = self.get_pos()
        self.win.move(y, 0)
        self.write_str(self.pad_string(''))

    def set_colors(self):
        self.colors = {
            'default': (0, 'COLOR_WHITE', 'COLOR_BLACK'),
            'title': (1, 'COLOR_YELLOW', 'COLOR_BLUE'),
            'status': (1, 'COLOR_YELLOW', 'COLOR_BLUE'),
            'error': (2, 'COLOR_RED', 'COLOR_BLACK'),
            'highlight': (3, 'COLOR_YELLOW', 'COLOR_BLACK'),
        }

        for color in self.colors.itervalues():
            if color[0] == 0: continue
            curses.init_pair(color[0], getattr(curses, color[1]), getattr(curses, color[2]))

    def pad_string(self, s):
        (maxy, maxx) = self.win.getmaxyx()
        return s + ' ' * (maxx - len(s) - 1)

    def get_color(self, type):
        if type in self.colors:
            return curses.color_pair(self.colors[type][0])
        else:
            return curses.color_pair(0)

def main(stdscr):
    screen = Screen(stdscr)

    locale.setlocale(locale.LC_ALL, '')
    screen.encoding = locale.getpreferredencoding()

    screen.set_title('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.set_status('Standby ready')

    screen.move(1, 0)

    counter = 0
    while True:
        c = screen.get_char()

        (y, x) = screen.get_pos()
        screen.set_status('[%i] (%i, %i) : %i' % (counter, y, x, c))

        counter += 1

        if c == curses.KEY_LEFT:
            (y, x) = screen.get_pos()
            screen.move(y, x-1)
        elif c == curses.KEY_RIGHT:
            (y, x) = screen.get_pos()
            screen.move(y, x+1)
        elif c == curses.KEY_RESIZE:
            screen.set_status('Resize')
        elif c == ord(':'):
            screen.read_command()
        elif c == curses.KEY_ENTER or c == curses.ascii.CR or c == curses.ascii.LF:
            (y, x) = screen.get_pos()
            screen.move(y+1, 0)


if __name__ == '__main__':
    curses.wrapper(main)

