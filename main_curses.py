# -*- coding: utf-8 -*-   

import sys
import curses
import curses.ascii
import locale

import common
import commands

locale.setlocale(locale.LC_ALL, '')

class Screen:
    def __init__(self, win):
        self.win = win
        self.set_colors()
        self.title = ''
        self.status = ''

    def write_str(self, s, attr = None):
        if attr is None: attr = curses.A_NORMAL
        (y, x) = self.win.getyx()
        self.win.addstr(s.encode(self.encoding), attr)

    def get_pos(self):
        return self.win.getyx()

    def get_size(self):
        return self.win.getmaxyx()

    def get_char(self):
        result = ''
        count = 0

        self.win.refresh()
        while True:       
            ch = self.win.getch()
            if ch == -1:
                return None 
            if ch > 255: 
                for attr in dir(curses):
                    if attr.startswith('KEY_') and getattr(curses, attr) == ch:
                        return '<%s>' % attr
                return '<%i>' % ch
            result += chr(ch)
            try:   
                return result.decode(self.encoding)
            except UnicodeDecodeError as e:
                count += 1
                # assumes multibytes characters are less that 4 bytes
                if count > 4 or e.reason != 'unexpected end of data':
                    return '?'


    def move(self, y, x):
        self.win.move(y, x)

    def set_title(self, s):
        self.title = s
        (y, x) = self.win.getyx()
        self.win.move(0, 0)
        self.write_str(self.pad_string(s), self.get_color('title') | curses.A_BOLD)
        self.win.move(y, x)

    def set_status(self, s):
        self.status = s
        (y, x) = self.win.getyx()
        (maxy, maxx) = self.win.getmaxyx()
        if maxy < 2: return
        self.win.move(maxy-2, 0)
        self.write_str(self.pad_string(s), self.get_color('status') | curses.A_BOLD)
        self.win.move(y, x)

    def refresh(self):
        self.set_title(self.title)
        self.set_status(self.status)
        self.win.refresh()

    def read_command(self):
        (maxy, maxx) = self.win.getmaxyx()
        (posy, posx) = self.win.getyx()
        if maxy < 1: return
        self.win.move(maxy-1, 0)

        self.write_str(':')
        cmd = ''

        count = 0
        while(True):
            count += 1
            c = self.get_char()
            if c is None:
                continue
            elif c == '<KEY_ENTER>' or c == '\n':
                break
            elif c == '<KEY_LEFT>':
                (y, x) = self.win.getyx()
                self.move(y, x-1)
            elif c == '<KEY_RIGHT>':
                (y, x) = self.win.getyx()
                self.move(y, x+1)
            else:
                # should be screen size
                if len(cmd) >= maxx - 2:
                    continue
                cmd += c
                self.write_str(c)
                self.set_status('%i/%i <%s> %i' % (len(cmd), maxx, c.strip(), count))

        self.handle_command(cmd)

        self.clear_line()
        self.move(posy, posx)

    def handle_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            sys.exit(0)

    def clear_line(self):
        (y, x) = self.win.getyx()
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
        #return s + ' ' * (maxx - len(s) - 1)
        return s.ljust(maxx - 1)

    def get_color(self, type):
        if type in self.colors:
            return curses.color_pair(self.colors[type][0])
        else:
            return curses.color_pair(0)

def main(stdscr):
    screen = Screen(stdscr)

    screen.encoding = locale.getpreferredencoding()

    screen.set_title('%s v%s' % (common.PROGNAME, common.PROGVERSION))
    screen.set_status('Standby ready')

    screen.move(1, 0)

    counter = 0
    while True:
        c = screen.get_char()

        if c is None:
            continue

        (y, x) = screen.get_pos()
        screen.set_status('[%i] (%i, %i) : <%s>' % (counter, y, x, c.strip()))

        counter += 1

        if c == '<KEY_LEFT>':
            (y, x) = screen.get_pos()
            screen.move(y, x-1)
        elif c == '<KEY_RIGHT>':
            (y, x) = screen.get_pos()
            screen.move(y, x+1)
        elif c == '<KEY_RESIZE>':
            screen.set_status('Resize')
            screen.refresh()
        elif c == ':':
            screen.read_command()
        elif c == '<KEY_ENTER>' or c == '\n':
            (y, x) = screen.get_pos()
            (maxy, maxx) = screen.win.getmaxyx()
            if y < maxy - 3:
                screen.move(y+1, 0)
        else:
            screen.write_str(c)


if __name__ == '__main__':
    curses.wrapper(main)

