import log

class CommandHandler(object):
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
                self.screen.refresh()
            elif c == '<KEY_UP>':
                self.screen.refresh()
            elif c == '<KEY_RESIZE>':
                self.screen.redraw()
            elif c == ':':
                cmd = self.screen.read_command()
                self.screen.set_status('(%i, %i) : <%s>' % (y, x, cmd.strip()))
                self.run_command(cmd)
            elif c == '<KEY_ENTER>' or c == '\n':
                self.screen.refresh()
            else:
                pass
                #screen.main.write(c)

    def run_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            self.screen.destroy()
        else:
            self.screen.main.add_line(cmd)
