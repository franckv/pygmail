from utils.base import BaseUtils
from utils.message import MessageUtils
from utils.recipient import RecipientUtils
from utils.tag import TagUtils
from utils.thread import ThreadUtils
from utils.db import DBUtils

class IndexUtils(BaseUtils):
    def __init__(self):
        super(IndexUtils, self).__init__()
        self.message = MessageUtils(self.session)
        self.recipient = RecipientUtils(self.session)
        self.tag = TagUtils(self.session)
        self.thread = ThreadUtils(self.session)
        self.db = DBUtils(self.session)

