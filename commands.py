import os, os.path

import config
import maildir
import utils

from indexmanager import IndexManager
from model import Base, Message, Thread, Tag, Path, Recipient

def get_index():
    return IndexManager()                                                                                                                                                  

def do_list():
    session = get_index().get_session()
    query = session.query(Message)

    for msg in query.all():
        print msg.id

    session.close()

def do_list_recipients():
    session = get_index().get_session()
    query = session.query(Recipient)

    for recipient in query.all():
        print recipient.__unicode__()

    session.close()

def do_delete(id):
    session = get_index().get_session()
    query = session.query(Message)
    msg = query.filter(Message.id == id).first()

    if not msg is None:
        session.delete(msg)
        session.commit()

    session.close()

def do_tag(id, tagname):
    session = get_index().get_session()
    query = session.query(Thread)
    thread = query.filter(Thread.id == id).first()

    tag = utils.lookup_tag(tagname, session)

    thread.tags.append(tag)

    session.commit()
    session.close()


def do_search(query):
    print('search: ' + query)

def do_reset():
    session = get_index().get_session()

    try:
        for cls in (Message, Thread, Tag, Path):
            if cls.__table__.exists(get_index().engine):
                query = session.query(cls)
                query.delete()

        session.commit()
    finally:
        session.close()

def do_create():
    index = get_index()
    
    Base.metadata.create_all(index.engine)

def do_drop():
    index = get_index()

    Base.metadata.drop_all(index.engine)

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


        session = get_index().get_session()
        query = session.query(Message)

        mails = maildir.get_mails(uri)
        for (uid, mail) in mails.items():

            msg = query.filter(Message.uid == uid).first()

            if msg is None:
                filename = mails.get_file(uid)._file.name
                (display, addr) = maildir.get_sender(mail)
                subject = maildir.get_subject(mail)

                msg = Message() 
                msg.uid = uid
                msg.sender = utils.lookup_recipient(display, addr, session)
                msg.subject = subject
                msg.path = Path(filename)
                msg.thread = Thread()

                session.add(msg)
            else:
                # assumes emails are immutable
                pass

        session.commit()
        session.close()


list = {
        'list': {'args': 0, 'exec': do_list},
        'list_recipients': {'args': 0, 'exec': do_list_recipients},
        'sync': {'args': 1, 'exec': do_sync},
        'reset': {'args': 0, 'exec': do_reset},
        'search': {'args': 1, 'exec': do_search},
        'delete': {'args': 1, 'exec': do_delete}
}

