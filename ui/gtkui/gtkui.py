import urllib
import urlparse
import os, sys
import gobject
import pygtk, gtk, gtk.glade, gtkhtml2

from utils import IndexUtils
from ui.gtkui.dialogs import TextEntryDialog
#import upload

class MainWindow(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)
        self.xml = gtk.glade.XML('ui/gtkui/ui.glade', 'MainWindow', 'pygmail')
        self.window = self.xml.get_widget('MainWindow')
        self.window.set_title('Pygmail')

        self.xml.signal_autoconnect(self)

        self.init_search_tab()

        self.msgViewHTML = gtkhtml2.View()
        self.msgViewHTML.connect('on_url', self.on_url)
        self.msgViewHTML.set_document(gtkhtml2.Document())

        scrolledMsgViewHTML = self.xml.get_widget('scrolledMsgViewHTML')
        scrolledMsgViewHTML.add(self.msgViewHTML)

        self.msgViewText = self.xml.get_widget('msgViewText')

        self.msgViewHeaders = self.xml.get_widget('msgViewHeaders')
        
        self.window.show_all()
        #self.window.connect('delete_event', self.on_quit)

        self.opener = urllib.FancyURLopener()
        self.currentUrl = None

    def is_relative_to_server(self, url):
        parts = urlparse.urlparse(url)
        if parts[0] or parts[1]:
            return 0
        return 1

    def open_url(self, url):
        uri = self.resolve_uri(url)
        print 'resolved:', uri
        return self.opener.open(uri)

    def resolve_uri(self, uri):
        if self.is_relative_to_server(uri):
            return urlparse.urljoin(self.currentUrl, uri)
        return uri

    def request_url(self, document, url, stream):
        print 'url requested:', url
        #f = self.open_url(url)
        #stream.write(f.read())

    def on_url(self, view, url):
        status = self.xml.get_widget('statusbar')
        if url != None:
            status.pop(0)
            status.push(0, url)
        else:
            status.pop(0)

    def request_object(self, *args):
        print 'request object', args

    def link_clicked(self, document, link):
        print 'link_clicked:', link
        #try:
        #    f = self.open_url(link)
        #except OSError:
        #    print "failed to open", link
        #    return
        #self.currentUrl = self.resolve_uri(link)
        #document.clear()
        #headers = f.info()
        #mime = headers.getheader('Content-type').split(';')[0]
        #if mime:
        #    document.open_stream(mime)
        #else:
        #    document.open_stream('text/plain')
        #document.write_stream(f.read())
        #document.close_stream()

    def init_search_tab(self):
        self.msgList = self.xml.get_widget('searchMsgList')

        tvcolumn = gtk.TreeViewColumn('Subject')
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)
        tvcolumn.set_sort_column_id(0)
        self.msgList.append_column(tvcolumn)

        tvcolumn = gtk.TreeViewColumn('Sender')
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 1)
        tvcolumn.set_sort_column_id(1)
        self.msgList.append_column(tvcolumn)

        treeselection = self.msgList.get_selection()
        treeselection.set_mode(gtk.SELECTION_MULTIPLE)

        listStore = gtk.ListStore(str, str, int, str)
        self.msgList.set_model(listStore)
        self.msgList.get_selection().connect('changed', self.on_selection_changed)

    def on_quit(self, widget=None, event=None): 
        self.window.hide()
        gtk.main_quit()
        gobject.timeout_add(200, os._exit, 0)
        sys.exit(0)

    def on_import(self, widget=None, event=None): 
        dialog = gtk.FileChooserDialog('Import', self.window,
            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            ('Cancel', gtk.RESPONSE_CANCEL,
            'Choose', gtk.RESPONSE_OK))

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            path = dialog.get_filename()
            dialog.destroy()

            (create, update) = upload.upload_dir(self.db, path)
            self.do_clear_search()

            status = self.xml.get_widget('statusbar')
            status.pop(1)
            status.push(1, '%i new, %i updated' % (create, update))
        else:
            dialog.destroy()

    def do_search(self, widget=None, event=None):
        listStore = self.msgList.get_model()
        self.msgList.set_model(None)

        tagsSearchEntry = self.xml.get_widget('tagsSearchEntry')
        tags = tagsSearchEntry.get_text()
        if tags != '':
            for tag in tags.split(' '):
                if tag != '':
                    pass

        nb = 0
        utils = IndexUtils()
        for msg in utils.message.get_messages():
            listStore.append([msg.subject, msg.sender.mail, msg.id, msg.path.path])
            nb += 1
        utils.close()
        status = self.xml.get_widget('statusbar')
        status.pop(1)
        status.push(1, str(nb) + ' messages')

        self.msgList.set_model(listStore)

    def do_clear_search(self, widget=None, event=None):
        listStore = self.msgList.get_model()
        listStore.clear()
        self.msgViewText.get_buffer().set_text('')
        self.msgViewHeaders.get_buffer().set_text('')
        self.msgViewHTML.set_document(gtkhtml2.Document())
        status = self.xml.get_widget('statusbar')
        status.pop(1)

    def format_headers(self, msg):
        buffer = ''
        #for header, value in msg.headers.iteritems():
        for header in sorted(msg.headers.keys()):
            values = msg.headers[header]
            for value in values:
                buffer += header + ": " + value + '\n'
        return buffer

    def set_msgView(self, msg, type=None):
        headers = self.format_headers(msg)
        if type == 'headers':
            body = ''
        else:
            body = msg.get_content(type)
            if body == '' and type == 'html':
                body = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
                body += '</head><body><pre>'
                body += msg.get_content('plain')
                body += '</pre></body></html>'
            
        if type == 'html':
            document = gtkhtml2.Document()
            document.connect('link_clicked', self.link_clicked)
            document.connect('request_url', self.request_url)
            document.open_stream('text/html')
            document.write_stream(body)
            document.close_stream()
            self.msgViewHTML.set_document(document)
        elif type == 'headers':
            buffer = self.msgViewHeaders.get_buffer().set_text(headers)
        else:
            buffer = self.msgViewText.get_buffer().set_text(body)

    def on_selection_changed(self, selection):
        selection = self.msgList.get_selection()
        if selection == None:
            return

        model, paths = selection.get_selected_rows()
        if paths and len(paths) == 1:
            path = paths[0]
            iter = model.get_iter(path)
            id = model.get_value(iter, 2)
            utils = IndexUtils()
            msg = utils.message.get(id)
            utils.close()
            #msg.open()
            self.set_msgView(msg, 'plain')
            self.set_msgView(msg, 'html')
            self.set_msgView(msg, 'headers')
            #msg.close()
            msgViewTabs = self.xml.get_widget('msgViewTabs')
            msgViewTabs.set_current_page(0)

    def on_tag_clicked(self, widget=None, event=None):
        selection = self.msgList.get_selection()
        if selection == None:
            return

        model, paths = selection.get_selected_rows()
        if paths and len(paths) == 1:
            path = paths[0]
            iter = model.get_iter(path)
            id = model.get_value(iter, 2)

            dialog = TextEntryDialog(self.window, "Tags", "Tag item")
            dialog.set_value(str(id))
            if dialog.run() == gtk.RESPONSE_OK:
                name = dialog.get_value()
                print name	
            dialog.destroy()

def run(args = None):
    win = MainWindow()
    gtk.main()

if __name__ == '__main__':
    run()
