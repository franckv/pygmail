from sqlalchemy import Table, Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relation, backref, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

thread_tag = Table('thread_tag', Base.metadata,
    Column('thread_id', Integer, ForeignKey('thread.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

message_to = Table('message_to', Base.metadata,
    Column('message_id', Integer, ForeignKey('message.id')),
    Column('recipient_id', Integer, ForeignKey('recipient.id'))
)

message_cc = Table('message_cc', Base.metadata,
    Column('message_id', Integer, ForeignKey('message.id')),
    Column('recipient_id', Integer, ForeignKey('recipient.id'))
)

class Path(Base):
    __tablename__ = 'path'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    message_id = Column(Integer, ForeignKey('message.id'))

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return "<Path('%s')>" % self.path

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag('%s')>" % self.name

class Thread(Base):
    __tablename__ = 'thread'

    id = Column(Integer, primary_key=True)
    tags = relation(Tag, secondary = thread_tag, backref=backref('threads', lazy='dynamic'))

    def __repr__(self):
        return "<Thread('%i')>" % self.id

class Recipient(Base):
    __tablename__ = 'recipient'
    id = Column(Integer, primary_key=True)
    displayname = Column(String)
    mail = Column(String, index=True, unique=True)

    def __init__(self, displayname, mail):
        self.displayname = displayname
        self.mail = mail

    def __unicode__(self):
        return "<Recipient '%s' %s>" % (self.displayname, self.mail)
       
class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    uid = Column(String, index=True, unique=True)
    subject = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey(Recipient.id))
    thread_id = Column(Integer, ForeignKey(Thread.id))
    read = Column(Boolean)
    delete = Column(Boolean)

    sender = relation(Recipient)
    path = relation(Path, uselist=False, backref=backref('message'), cascade='all, delete, delete-orphan')
    thread = relation(Thread, backref=backref('messages'))
    tos = relation(Recipient, secondary = message_to, )
    ccs = relation(Recipient, secondary = message_cc, )

    def __init__(self):
        self.headers = {}

    def __repr__(self):
        return "<Message('%s','%s')>" % (self.sender.mail, self.subject)


    @validates(sender)
    def validate_email(self, key, address):
        assert '@' in address
