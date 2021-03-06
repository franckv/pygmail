import os.path
import re

from email import header, utils
from mailbox import Maildir, MaildirMessage

import config

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

def get_header(mail, var):
    result = ''
    value = mail.get(var)
    for (decoded, enc) in header.decode_header(value):
        if enc:
            decoded = unicode(decoded, enc)
        else:
            try:
                decoded = unicode(decoded)
            except:
                decoded =  unicode(decoded, config.default_encoding)

        result += decoded
        
    return result

def get_sender(mail):
    sender = get_header(mail, 'From')
    return utils.parseaddr(sender)

def get_subject(mail):
    return get_header(mail, 'Subject')

def get_mails(uri):
#    files = os.listdir(uri)
#
#    for file in files:
#       filepath = os.path.join(uri, file)
#       mail = maildir.get_mail(filepath)

    md = Maildir(uri, factory=None)

    return md

def get_mail(filename):
    if not os.path.exists(filename):
        return None

    msg = open(filename)
    mail = MaildirMessage(msg)
    msg.close()
    return mail

def get_content(mail, type = None):
    content = ''
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart' \
            or part.get_content_maintype() == 'message':
            continue

        if type != None and type != 'raw' and part.get_content_subtype() != type:
            continue

        content_type = part.get_content_type()
        #content += content_type + '\n'

        filename = part.get_filename()
        if filename:
            content += filename + '\n'
            continue

        if part.get_content_maintype() != 'text':
            continue

        found = True
        payload = part.get_payload(decode=True)
        if part.get_content_charset() != None:
            #content += part.get_content_charset() + '\n'
            payload = payload.decode(part.get_content_charset())
            if type == 'html':
                payload = payload.encode(part.get_content_charset())
            else:
                payload = payload.encode('utf8')
        else:
            #TODO: get this from the user interface
            defaultencoding = 'iso-8859-1'
            payload = payload.decode(defaultencoding).encode('utf8')
            content += payload
    return content

