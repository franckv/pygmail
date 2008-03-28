from message import Message

class SQLConnector():
    def __init__(self, engine, host, db, user, passwd):
	self.con = None
	self.engine = engine
	self.host = host
	self.db = db
	self.user = user
	self.passwd = passwd

    def connect(self):
	if self.engine == 'sqlite':
	    import sqlite3
	    self.con = sqlite3.connect(self.db)
	elif engine == 'mysql':
	    import MySQLdb
	    self.con = MySQLdb.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd, use_unicode=True)

    def get_messages(self, tags):
	results = {}
	self.connect()
	cur = self.con.cursor()
	if len(tags) == 0:
	    print 'no search tags'
	    cur.execute('select message.id, message.sender, message.subject, path.path ' \
		    'from message, path ' \
		    'where message.id = path.message_id;')
	else:
	    taglist = ''
	    for tag in tags:
		if taglist != '':
		    taglist += ',';
		taglist += "'" + tag + "'"
	    print taglist
	    cur.execute('select ' \
		    'message.id, message.sender, message.subject, path.path ' \
		    'from message, path, message_tag, tag ' \
		    'where message.id = path.message_id and message_tag.tag_id = tag.id ' \
		    'and message.id = message_tag.message_id ' \
		    'and tag.name in (' + taglist + ');')

	for row in cur.fetchall():
	    id = row[0]
	    sender = row[1]
	    subject = row[2]
	    path = row[3]
	    #tag = row[4]
	    msg = Message(id)
	    msg.put_header('From', sender)
	    msg.put_header('Subject', subject)
	    msg.set_path(path)
	    #msg.put_tag(tag)
	    results[id] = msg
	cur.close()
	self.close()

	return results

    def close(self):
	self.con.close()

    def get_all_tags(self):
	results = []
	cur = self.con.cursor()
	cur.execute('select name from tag')
	for row in cur.fetchall():
	    results.push(row[0])
	cur.close()

    def message_add_tag(self, id, tag):
	pass
