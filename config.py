#engine = 'sqlite:///:memory:'
engine = 'sqlite:////home/franck/Dev/pygmail/db/pygmail.db'

stores = {
    #'IMAP': {'type': 'maildir', 'uri': '/home/franck/Mail/IMAP'}
    'Comptes': {'type': 'maildir', 'uri': '/home/franck/Mail/IMAP/Autres.Comptes'}
    #'All': {'type': 'maildir', 'uri': '/home/franck/Mail/IMAP/[Gmail].All Mail'}
}

default_encoding = 'latin1'
