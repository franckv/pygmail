from db import SQLConnector
from message import Message

class Query():
    def __init__(self):
	self.messages = {}
	self.querytags = []

    def get_message(self, id):
	if not self.messages.has_key(id):
	    return None
	else:
	    return self.messages[id]

    def add_query_tag(self, tag):
	self.querytags.append(tag)

    def getMsgList(self, store):
	store.clear()

	con = SQLConnector()
	con.connect('sqlite', '', 'db/pygmail.db', '', '')
	self.messages = con.get_messages(self.querytags)
	con.close()

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
