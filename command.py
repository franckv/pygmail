import os, os.path

import config

from model import Message, Thread, Tag, Path
from mbox import maildir
from utils.index import IndexUtils

def do_list():
    utils = IndexUtils()

    ids = utils.message.get_ids()

    for id in ids: print(id)

    utils.close()

def do_list_recipients():
    utils = IndexUtils()

    recipients = utils.recipient.get_recipients()

    for recipient in recipients:
        print(recipient.__unicode__())

    utils.close()

def do_list_tags():
    utils = IndexUtils()

    tags = utils.tag.get_tags()

    for tag in tags:
        print(tag.__unicode__())

    utils.close()

def do_show(id):
    utils = IndexUtils()
    msg = utils.message.get(id)
    utils.close()

    if msg:
        print(msg.path.path)
        mail = maildir.get_mail(msg.path.path)
        content = maildir.get_content(mail)
    else:
        print('Not found')

def do_delete(id):
    utils = IndexUtils()

    utils.message.delete(id)

    utils.close()

def do_tag(id, tagname):
    utils = IndexUtils()

    utils.thread.add_tag(id, tagname)

    utils.close()


def do_search(query):
    print('search: ' + query)

def do_reset():
    utils = IndexUtils()

    for cls in (Message, Thread, Tag, Path):
        utils.db.truncate(cls)

    utils.close()

def do_create():
    utils = IndexUtils()
    utils.db.create()
    utils.close()

def do_drop():
    utils = IndexUtils()
    utils.db.drop()
    utils.close()

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
        utils = IndexUtils()

        # TODO: move that to a maildir utils interface
        mails = maildir.get_mails(uri)
        for (uid, mail) in mails.items():
            if not utils.message.exists(uid):
                filename = mails.get_file(uid)._file.name
                (display, addr) = maildir.get_sender(mail)
                subject = maildir.get_subject(mail)

                msg = Message() 
                msg.uid = uid
                msg.sender = utils.recipient.lookup_recipient(display, addr, True)
                msg.subject = subject
                msg.path = Path(filename)
                msg.thread = Thread()

                utils.message.add(msg)
            else:
                # assumes emails are immutable
                pass

        utils.close()

list = {
        'list': {'args': 0, 'exec': do_list},
        'list_recipients': {'args': 0, 'exec': do_list_recipients},
        'list_tags': {'args': 0, 'exec': do_list_tags},
        'show': {'args': 1, 'exec': do_show},
        'sync': {'args': 1, 'exec': do_sync},
        'reset': {'args': 0, 'exec': do_reset},
        'drop': {'args': 0, 'exec': do_drop},
        'create': {'args': 0, 'exec': do_create},
        'search': {'args': 1, 'exec': do_search},
        'delete': {'args': 1, 'exec': do_delete}
}

