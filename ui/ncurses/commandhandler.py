import log
import re
import curses

from .widget import TextPanel
from utils.index import IndexUtils

class CommandHandler(object):
    def __init__(self, screen):
        self.screen = screen
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

            events = ['<KEY_LEFT>', '<KEY_RIGHT>', '<KEY_DOWN>', '<KEY_UP>', '<KEY_RESIZE>', '<KEY_ENTER>', '<KEY_BACKSPACE>', '<KEY_TAB>', '<KEY_BTAB>']

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
            elif c == 'd':
                tab_name = self.screen.main.current.name
                if tab_name.startswith('msg'):
                    log.debug('deleting tab %s' % tab_name)
                    self.screen.main.delete_tab()
                    self.screen.update_title()
            elif c == 'D':
                tab_name = self.screen.main.current.name
                if tab_name == 'list':
                    selected = self.screen.main.current.selected
                    if not selected is None:
                        id = self.msgs[selected].id
                        del self.msgs[selected]
                        self.screen.main.current.clear_lines()
                        for msg in self.msgs: self.screen.main.current.add_line('[%i] %s' % (msg.id, msg.subject))
                        log.debug('deleting message %i' % selected)
                        utils = IndexUtils()
                        utils.message.delete(id)
                        utils.close()
            else:
                log.debug('unknown command %s' % c)

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
            self.screen.main.show_tab('list')
            self.screen.main.current.clear_lines()

            utils = IndexUtils()
            self.msgs = utils.message.get_messages(limit)
            for msg in self.msgs: self.screen.main.current.add_line('[%i] %s' % (msg.id, msg.subject))
            utils.close()
            self.screen.set_status('%i results' % len(self.msgs))
            self.screen.update_title()
        elif cmd.startswith('delete '):
                id = int(cmd[7:])
                for msg in self.msgs:
                    if msg.id == id:
                        self.msgs.remove(msg)
                        self.screen.main.current.clear_lines()
                        for msg in self.msgs: self.screen.main.current.add_line('[%i] %s' % (msg.id, msg.subject))
                        break
                utils = IndexUtils()
                utils.message.delete(id)
                utils.close()

        elif cmd == 'clear':
            self.screen.main.current.clear_lines()
            self.screen.set_status('cleared')
        else:
            pass

    def run_search(self, search):
        pass

    def item_selected(self, idx):
        msg = self.msgs[idx]
        tab_name ='msg%i' % msg.id 
        if not tab_name in self.screen.main.tabs:
            msg_panel = self.screen.main.create_tab(TextPanel, 'msg%i' % msg.id)
            msg_panel.add_line(msg.subject)
        self.screen.main.show_tab('msg%i' % msg.id)
        self.screen.update_title()


