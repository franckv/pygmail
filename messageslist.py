from db import SQLConnector
from message import Message

class Query():
    def __init__(self, db):
	self.messages = {}
	self.querytags = []
	self.db = db

    def get_message(self, id):
	if not self.messages.has_key(id):
	    return None
	else:
	    return self.messages[id]

    def add_query_tag(self, tag):
	self.querytags.append(tag)

    def getMsgList(self, store):
	store.clear()

	self.messages = self.db.get_messages(self.querytags)

	nb = 0
	for mail in self.messages.itervalues():
	    sender = mail.get_header('From')
	    subject = mail.get_header('Subject')
	    #tags = mail.get_tags()
	    #print tags
	    iter = store.append([subject, sender, mail.id, mail.get_path()])
	    nb += 1
	
	print '%s messages read from db' % (nb)
	return nb
