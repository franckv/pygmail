import os.path
import dircache
from optparse import OptionParser
from mailbox import mbox
from email import header
#import MySQLdb
import sqlite3

def insert_id(cur):
    cur.execute('SELECT LAST_INSERT_ROWID()')
    row = cur.fetchone()
    return row[0]

def decode_header(mail, var):
    result = ''
    for (decoded, enc) in header.decode_header(mail.get(var)):
	if enc:
	    decoded = decoded.decode(enc)
	result += decoded

    return result

def upload_mail(conn, sender, subject, path):
    cur = conn.cursor()
    cur.execute('INSERT INTO message (sender, subject, account, read) VALUES (?, ?, 1, 0);', (sender.encode('utf8'), subject.encode('utf8')))
    id = insert_id(cur)
    cur.execute('INSERT INTO path (message_id, path) VALUES ("%i", ?);' % (id,), (path.encode('utf8'),))
    cur.close()

parser = OptionParser()
parser.add_option("-d", dest="dirname")

(options, args) = parser.parse_args()

if options.dirname == None:
    exit()

maildir = os.path.abspath(options.dirname)

list = dircache.listdir(maildir)

#conn = MySQLdb.connect('localhost', 'pygmail', 'pygmail', 'pygmail')
conn = sqlite3.connect('../db/pygmail.db')
#conn.charset = 'utf8'

for file in list:
    filename = maildir + os.sep + file

    mails = mbox(filename)
    for mail in mails:
	if mail != None:
	    sender = decode_header(mail, 'From')
	    subject = decode_header(mail, 'Subject')
	    #print sender, subject
	    upload_mail(conn, sender, subject, filename)

conn.commit()
conn.close()
