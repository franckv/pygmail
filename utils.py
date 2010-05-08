from model import Recipient, Tag
from indexmanager import IndexManager


def lookup_recipient(display, mail, session):
    query = session.query(Recipient)

    recipient = query.filter(Recipient.mail == mail).first()
    if recipient is None:
        recipient = Recipient(display, mail)
        session.add(recipient)

    return recipient


def lookup_tag(tagname, session):
    query = session.query(Tag)

    tag = query.filter(Tag.name == tagname).first()
    if tag is None:
        tag = Tag(tagname)
        session.add(tag)

    return tag

