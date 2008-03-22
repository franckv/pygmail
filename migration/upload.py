import os.path
import dircache
from optparse import OptionParser
from mailbox import mbox
from email import header
import MySQLdb

def decode_header(mail, var):
    result = ''
    for (decoded, enc) in header.decode_header(mail.get(var)):
	if enc:
	    decoded = decoded.decode(enc)
	result += decoded

    return result

def upload_mail(conn, sender, subject, path):
    cur = conn.cursor()
    cur.execute('INSERT INTO message (message.from, message.subject, message.account, message.read) VALUES (%s, %s, "1", "0");', (sender.encode('utf8'), subject.encode('utf8')))
    id = conn.insert_id()
    cur.execute('INSERT INTO path (path.message_id, path.path) VALUES ("%i", %%s);' % (id,), (path.encode('utf8'),))
    cur.close()

parser = OptionParser()
parser.add_option("-d", dest="dirname")

(options, args) = parser.parse_args()

if options.dirname == None:
    exit()

maildir = os.path.abspath(options.dirname)

list = dircache.listdir(maildir)

conn = MySQLdb.connect('localhost', 'pygmail', 'pygmail', 'pygmail')
conn.charset = 'utf8'

for file in list:
    filename = maildir + os.sep + file

    mails = mbox(filename)
    for mail in mails:
	if mail != None:
	    sender = decode_header(mail, 'From')
	    subject = decode_header(mail, 'Subject')
	    #print sender, subject
	    upload_mail(conn, sender, subject, filename)

conn.close()
