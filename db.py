from message import Message

class SQLConnector():
    def __init_(self):
	self.con = None

    def connect(self, engine, host, db, user, passwd):
	self.engine = engine
	if engine == 'sqlite':
	    import sqlite3
	    self.con = sqlite3.connect(db)
	elif engine == 'mysql':
	    import MySQLdb
	    self.con = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd, use_unicode=True)

    def get_messages(self, tags):
	results = {}
	cur = self.con.cursor()
	if len(tags) == 0:
	    cur.execute('select message.id, message.sender, message.subject, path.path, tag.name ' \
		'from message, path, message_tag, tag ' \
		'where message.id = path.message_id and message_tag.tag_id = tag.id ' \
		'and message.id = message_tag.message_id ' \
		'union select message.id, message.sender, message.subject, path.path, \'\' ' \
		'from message, path, message_tag, tag;')
	else:
	    taglist = ''
	    for tag in tags:
		if taglist != '':
		    taglist += ',';
		taglist += "'" + tag + "'"
	    print taglist
	    cur.execute('select ' \
		    'message.id, message.sender, message.subject, path.path, tag.name ' \
		    'from message, path, message_tag, tag ' \
		    'where message.id = path.message_id and message_tag.tag_id = tag.id ' \
		    'and message.id = message_tag.message_id ' \
		    'and tag.name in (' + taglist + ');')
		    #'and message.id in ' \
		    #'(select message_tag.message_id ' \
		    #' from message_tag ' \
		    #'where message_tag.tag_id in ' \
		    #'(select tag.id from tag where tag.name in ' \
		    #'(' + taglist + ')));')

	for row in cur.fetchall():
	    id = row[0]
	    sender = row[1]
	    subject = row[2]
	    path = row[3]
	    tag = row[4]
	    msg = Message(id)
	    msg.put_header('From', sender)
	    msg.put_header('Subject', subject)
	    msg.set_path(path)
	    msg.put_tag(tag)
	    results[id] = msg
	cur.close()

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
