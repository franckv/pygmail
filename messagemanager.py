import re

from email import header
from mailbox import mbox

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

class Message():
    def __init__(self, id = 0):
        self.headers = {}
        self.subject = None
        self.sender = None
        self.id = id
        self.path = ''
        self.mail = None
        self.tags = []

    def open(self):
        if self.mail != None:
            return
        mails = mbox(self.path)
        for mail in mails:
            if mail != None:
                self.mail = mail
                self.parse_headers()
                return
        print 'message not found:', self.path

    def close(self):
        self.mail = None

    def parse_headers(self):
        self.headers = {}
        for (header, value) in self.mail.items():
            value = self.decode_header(value)
            if not header in self.headers:
                self.headers[header] = [value]
            else:
                self.headers[header].append(value)

    def get_tags(self):
        return self.tags

    def put_tag(self, tag):
        self.tags.append(tag)
	
    def get_header(self, header):
        if header in self.headers:
            return self.headers[header][0]
        else:
            return None

    def set_sender(self, value):
        self.sender = value

    def get_sender(self):
        return self.sender

    def set_subject(self, value):
        self.subject = value

    def get_subject(self):
        return self.subject

    def put_header(self, header, value):
        if not header in self.headers:
            self.headers[header] = [value]
        else:
            self.headers[header].append(value)

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def decode_header(self, value):
        result = ''
        for (decoded, enc) in header.decode_header(value):
            if enc:
            decoded = decoded.decode(enc)
            result += decoded

        return result

    def get_content(self, type):
        content = ''
        if self.mail == None:
            return content

        for part in self.mail.walk():
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

