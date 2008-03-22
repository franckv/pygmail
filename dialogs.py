import os, sys
import gobject
import pygtk, gtk, gtk.glade

class TextEntryDialog(object):
    """
        Shows a dialog with a single line of text
    """
    def __init__(self, parent, message, title):
        """
            Initializes the dialog
        """
        self.parent = parent
        xml = gtk.glade.XML('ui/pygmail.glade', 'TextEntryDialog', 'pygmail')
        self.dialog = xml.get_widget('TextEntryDialog')
        xml.get_widget('ted_question_label').set_label(message)
        self.dialog.set_title(title)
        self.dialog.set_transient_for(parent)

        xml.get_widget('ted_cancel_button').connect('clicked',
            lambda e: self.dialog.response(gtk.RESPONSE_CANCEL))

        self.entry = xml.get_widget('ted_entry')
        xml.get_widget('ted_ok_button').connect('clicked',
            lambda e: self.dialog.response(gtk.RESPONSE_OK))
        self.entry.connect('activate',
            lambda e: self.dialog.response(gtk.RESPONSE_OK))

    def run(self):
        """
            Runs the dialog, waiting for input
        """
        return self.dialog.run()

    def get_value(self):
        """
            Returns the text value
        """
        return self.entry.get_text()

    def set_value(self, value):
        """
            Sets the value of the text
        """
        self.entry.set_text(value)

    def destroy(self):
        """
            Destroys the dialog
        """
        self.dialog.destroy()

