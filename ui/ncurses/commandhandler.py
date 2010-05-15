import log
import re
import curses

from utils import IndexUtils

class CommandHandler(object):
    def __init__(self, screen):
        self.screen = screen
        screen.set_handler(self)
        self.buf = ''

    def handle(self):
        curses.curs_set(0)
        while True:
            c = self.screen.get_char()
            log.debug(c)

            if c is None:
                continue


            (y, x) = self.screen.get_pos()
            self.screen.set_status('(%i, %i) : <%s>' % (y, x, c.strip()))

            events = ['<KEY_LEFT>', '<KEY_RIGHT>', '<KEY_DOWN>', '<KEY_UP>', '<KEY_RESIZE>', '<KEY_ENTER>', '<KEY_BACKSPACE>']

            if c in events:
                self.screen.send_event(c)
            elif c == ':':
                cmd = self.screen.read_command()
                self.screen.set_status('(%i, %i) : <%s>' % (y, x, cmd.strip()))
                self.run_command(cmd)
            elif c == '/':
                search = self.screen.read_search()
                self.screen.set_status('(%i, %i) : <%s>' % (y, x, search.strip()))
                self.run_search(search)
            else:
                pass

    def run_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            self.screen.destroy()
        elif cmd == 'l' or cmd == 'list' or cmd.startswith('list '):
            limit = 15
            if cmd.startswith('list '):
                try:
                    limit = int(cmd[4:])
                except:
                    pass
            self.screen.main.clear_lines()

            utils = IndexUtils()
            msgs = utils.message.get_messages(limit)
            for msg in msgs: self.screen.main.add_line('[%i] %s' % (msg.id, msg.subject))
            utils.close()
            self.screen.set_status('%i results' % len(msgs))
        elif cmd == 'clear':
            self.screen.main.clear_lines()
            self.screen.set_status('cleared')
        else:
            pass

    def run_search(self, search):
        pass
