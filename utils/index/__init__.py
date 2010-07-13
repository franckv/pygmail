from base import BaseUtils
from message import MessageUtils
from recipient import RecipientUtils
from tag import TagUtils
from thread import ThreadUtils
from db import DBUtils

class IndexUtils(BaseUtils):
    def __init__(self):
        super(IndexUtils, self).__init__()
        self.message = MessageUtils(self.session)
        self.recipient = RecipientUtils(self.session)
        self.tag = TagUtils(self.session)
        self.thread = ThreadUtils(self.session)
        self.db = DBUtils(self.session)

