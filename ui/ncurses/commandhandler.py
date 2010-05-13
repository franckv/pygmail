import log

class CommandHandler:
    def __init__(self, screen):
        self.screen = screen
        screen.set_handler(self)
        self.buf = ''

    def handle(self):
        while True:
            c = self.screen.get_char()
            log.debug(c)

            if c is None:
                continue

            (y, x) = self.screen.get_pos()
            self.screen.set_status('(%i, %i) : <%s>' % (y, x, c.strip()))
            if c == '<KEY_LEFT>':
                (y, x) = self.screen.get_pos()
                self.screen.move(y, x-1)
            elif c == '<KEY_RIGHT>':
                (y, x) = self.screen.get_pos()
                self.screen.move(y, x+1)
            elif c == '<KEY_DOWN>':
                self.screen.win.scroll(1)
                self.screen.refresh()
            elif c == '<KEY_UP>':
                self.screen.win.scroll(-1)
                self.screen.refresh()
            elif c == '<KEY_RESIZE>':
                self.screen.resize()
            elif c == ':':
                cmd = self.screen.read_command()
                self.screen.set_status('(%i, %i) : <%s>' % (y, x, cmd.strip()))
                self.run_command(cmd)
            elif c == '<KEY_ENTER>' or c == '\n':
                (y, x) = self.screen.get_pos()
                (maxy, maxx) = self.screen.win.getmaxyx()
                if y < maxy - 3:
                    self.screen.move(y+1, 0)
            else:
                pass
                #screen.main.write(c)

    def run_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            self.screen.destroy()

