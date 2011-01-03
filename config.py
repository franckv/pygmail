#engine = 'sqlite:///:memory:'
engine = 'sqlite:////home/franck/Dev/pygmail/db/pygmail.db'

stores = {
    #'IMAP': {'type': 'maildir', 'uri': '/home/franck/Mail/IMAP'}
    'Comptes': {'type': 'maildir', 'uri': '/home/franck/Mail/IMAP/Autres.Comptes'}
    #'All': {'type': 'maildir', 'uri': '/home/franck/Mail/IMAP/[Gmail].All Mail'}
}

default_encoding = 'latin1'

colors = {
    #'default': (0, 'WHITE', 'BLACK', 'NORMAL'),
    'default': (0, 'RED', 'BLACK', 'NORMAL'),
    'title': (1, 'YELLOW', 'BLUE', 'BOLD'),
    'status': (2, 'YELLOW', 'BLUE', 'BOLD'),
    'error': (3, 'RED', 'BLACK', 'BOLD'),
    'highlight': (4, 'YELLOW', 'MAGENTA', 'BOLD'),
    'deleted': (5, 'RED', 'BLACK', 'NORMAL'),
} 
