import os, os.path

import config
import maildir

from model import Message, Thread, Tag, Path
from utils import MessageUtils, RecipientUtils, DBUtils, TagUtils

def do_list():
    utils = MessageUtils()

    ids = utils.get_ids()

    for id in ids: print id 

    utils.close()

def do_list_recipients():
    utils = RecipientUtils()

    recipients = utils.get_recipients()

    for recipient in recipients:
        print recipient.__unicode__()

    utils.close()

def do_list_tags():
    utils = TagUtils()

    tags = utils.get_tags()

    for tag in tags:
        print tag.__unicode__()

    utils.close()

def do_delete(id):
    utils = MessageUtils()

    utils.delete(id)

    utils.close()

def do_tag(id, tagname):
    utils = ThreadUtils()

    utils.add_tag(id, tagname)

    utils.close()


def do_search(query):
    print('search: ' + query)

def do_reset():
    utils = DBUtils()

    for cls in (Message, Thread, Tag, Path):
        utils.truncate(cls)

    utils.close()

def do_create():
    DBUtils.create()

def do_drop():
    DBUtils.drop()

def do_sync(name):

    if not name in config.stores:
        print('Invalid store')
    else:
        print('Syncing %s' % name)

        store = config.stores[name]
        uri = store['uri']

        if not os.path.exists(uri):
            print('Invalid uri: %s' % uri)
            return

        # TODO: merge service interfaces
        messageutils = MessageUtils()
        recipientutils = RecipientUtils(messageutils.session)

        # TODO: move that to a maildir utils interface
        mails = maildir.get_mails(uri)
        for (uid, mail) in mails.items():
            if not messageutils.exists(uid):
                filename = mails.get_file(uid)._file.name
                (display, addr) = maildir.get_sender(mail)
                subject = maildir.get_subject(mail)

                msg = Message() 
                msg.uid = uid
                msg.sender = recipientutils.lookup_recipient(display, addr)
                msg.subject = subject
                msg.path = Path(filename)
                msg.thread = Thread()

                messageutils.add(msg)
            else:
                # assumes emails are immutable
                pass

        messageutils.close()

list = {
        'list': {'args': 0, 'exec': do_list},
        'list_recipients': {'args': 0, 'exec': do_list_recipients},
        'list_tags': {'args': 0, 'exec': do_list_tags},
        'sync': {'args': 1, 'exec': do_sync},
        'reset': {'args': 0, 'exec': do_reset},
        'search': {'args': 1, 'exec': do_search},
        'delete': {'args': 1, 'exec': do_delete}
}

