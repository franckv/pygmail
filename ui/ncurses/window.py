import log
from widget.screen import Screen
from widget.statusbar import StatusBar
from widget.commandbar import CommandBar
from widget.titlebar import TitleBar
from widget.panel import Panel
from widget.textpanel import TextPanel
from widget.itemlist import ItemList

class Window(Screen):
    def __init__(self, win):
        super(Window, self).__init__(win)

        self.status = StatusBar(self)
        self.title = TitleBar(self)
        self.main = ItemList(self)
        self.command = CommandBar(self)

        self.register_event('<KEY_RESIZE>', self.redraw)

    def set_handler(self, handler):
        self.handler = handler

    def set_status(self, text):
        self.status.set_text(text)

    def set_title(self, text):
        self.title.set_text(text)

    def get_char(self):
        return self.command.get_char()

    def read_command(self):
        return self.command.read(':', self.validate_command_input)

    def read_search(self):
        return self.command.read('/', self.validate_command_input)

    def validate_command_input(self, c):
        (y, x) = self.command.get_pos()
        self.set_status('(%i, %i) : <%s>' % (y, x, c.strip()))
    
        return True


