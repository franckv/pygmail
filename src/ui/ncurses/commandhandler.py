import logging
import curses

from pycurses_widgets import TextPanel
from utils.index import IndexUtils

class CommandHandler(object):
    def __init__(self, screen):
        self.screen = screen
        self.buf = ''
        self.show_deleted = True

    def delete_tab(self, event):
        tab_name = self.screen.main.current.name
        if tab_name.startswith('msg'):
            logging.debug('deleting tab %s' % tab_name)
            self.screen.main.delete_tab()
            self.screen.update_title()

    def toggle_show_deleted(self, event):
        self.show_deleted = not self.show_deleted
        self.do_refresh(None)

    def delete_message(self, event):
        tab_name = self.screen.main.current.name
        if tab_name == 'list':
            selected = self.screen.main.current.selected
            if not selected is None:
                logging.debug('deleting message %i' % selected)
                id = self.msgs[selected].id
                self.do_delete(id)

    def undo_delete(self, event):
        tab_name = self.screen.main.current.name
        if tab_name == 'list':
            selected = self.screen.main.current.selected
            if not selected is None:
                logging.debug('undeleting message %i' % selected)
                id = self.msgs[selected].id
                self.do_undelete(id)

    def run_command(self, event):
        line = self.screen.read(event)
        if ' ' in line:
            (cmd, args) = line.split(' ', 1)
        else:
            cmd = line
            args = None

        if cmd in self.commands:
            self.commands[cmd]['exec'](self, args)

    def run_search(self, event):
        search = self.screen.read(event)

    def item_selected(self, idx):
        msg = self.msgs[idx]
        tab_name ='msg%i' % msg.id 
        if not tab_name in self.screen.main.tabs:
            msg_panel = self.screen.main.create_tab(TextPanel, 'msg%i' % msg.id)
            msg_panel.add_line(msg.subject)
        self.screen.main.show_tab('msg%i' % msg.id)
        self.screen.update_title()


    def do_quit(self, args):
        self.screen.destroy()

    def do_list(self, args):
        limit = 16
        if args:
            try:
                limit = int(args)
            except:
                pass
        self.screen.main.show_tab('list')

        utils = IndexUtils()
        self.msgs = utils.message.get_messages(limit)
        utils.close()
        self.do_refresh(None)
        self.screen.set_status('%i results' % len(self.msgs))
        self.screen.update_title()

    def do_delete(self, args):
        id = int(args)
        for msg in self.msgs:
            if msg.id == id:
                msg.delete = True
                utils = IndexUtils()
                utils.message.delete(msg.id)
                utils.close()
                #self.msgs.remove(msg)
                self.do_refresh(None)
                break

    def do_undelete(self, args):
        id = int(args)
        for msg in self.msgs:
            if msg.id == id:
                msg.delete = False
                utils = IndexUtils()
                utils.message.undelete(msg.id)
                utils.close()
                #self.msgs.remove(msg)
                self.do_refresh(None)
                break

    def do_refresh(self, args):
        self.screen.main.current.clear_lines()
        for msg in self.msgs:
            if msg.delete and self.show_deleted:
                style = 'deleted'
            elif msg.delete:
                style = 'hidden'
            else:
                style = 'default'
            self.screen.main.current.add_line('[%i] %s' % (msg.id, msg.subject), style)

    def do_clear(self, args):
        self.screen.main.current.clear_lines()
        self.screen.set_status('cleared')

    commands = {
            'c': {'exec': do_clear},
            'clear': {'exec': do_clear},

            'd': {'exec': do_delete},
            'delete': {'exec': do_delete},

            'l': {'exec': do_list},
            'list': {'exec': do_list},

            'q': {'exec': do_quit},
            'quit': {'exec': do_quit},

            'refresh': {'exec': do_refresh},

            'undelete': {'exec': do_undelete},
}
