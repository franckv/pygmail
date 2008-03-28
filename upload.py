import os.path
import dircache
import re

from mailbox import mbox
from email import header
from email import Utils

header.ecre = re.compile(r'''
  =\?                   # literal =?
  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset
  \?                    # literal ?
  (?P<encoding>[qb])    # either a "q" or a "b", case insensitive
  \?                    # literal ?
  (?P<encoded>.*?)      # non-greedy up to the next ?= is the encoded string
  \?=                   # literal ?=
  #(?=[ \t]|$)           # whitespace or the end of the string
  ''', re.VERBOSE | re.IGNORECASE | re.MULTILINE) 

def decode_header(mail, var):
    result = ''
    value = mail.get(var)
    for (decoded, enc) in header.decode_header(value):
	if enc:
	    decoded = decoded.decode(enc)
	result += decoded

    return result

def upload_mail(db, sender, subject, path):
    cur = db.cursor()
    cur.execute('SELECT message_id from path WHERE path=?', (path,))
    row = cur.fetchone()
    new = False
    if not row:
	new = True
	cur.execute('INSERT INTO message (sender, subject, account, read) VALUES (?, ?, 1, 0);',
		(sender.encode('utf8'), subject.encode('utf8')))
	id = db.insert_id()
	cur.execute('INSERT INTO path (message_id, path) VALUES ("%i", ?);' % id, (path.encode('utf8'),))
    else:
	cur.execute('UPDATE message SET sender=?, subject=?, account=1, read=0 WHERE id=%i;' % row[0],
		(sender.encode('utf8'), subject.encode('utf8')))
    cur.close()
    return new

def upload_dir(db, dirname):
    maildir = os.path.abspath(dirname)

    list = dircache.listdir(maildir)

    db.connect()

    create = 0
    update = 0
    for file in list:
	filename = maildir + os.sep + file

	mails = mbox(filename)
	for mail in mails:
	    if mail != None:
		sender = decode_header(mail, 'From')
		(display, addr) = Utils.parseaddr(sender)
		subject = decode_header(mail, 'Subject')
		#print sender, subject
		new = upload_mail(db, addr, subject, filename)
		if new:
		    create += 1;
		else:
		    update += 1;

    db.commit()
    db.close()

    return (create, update)
