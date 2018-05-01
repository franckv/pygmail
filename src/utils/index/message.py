from model import Message
from . import BaseUtils

class MessageUtils(BaseUtils):
    def __init__(self, session = None):
        super(MessageUtils, self).__init__(session)
        self.query = self.session.query(Message)

    def get_ids(self):
        results = []

        for msg in self.query.all():
            results.append(msg.id)

        return results

    def get(self, id):
        msg = self.query.filter(Message.id == id).first()
        return msg

    def get_messages(self, limit = 10):
        results = []

        for msg in self.query.limit(limit).all():
            results.append(msg)

        return results

    def exists(self, uid):
        msg = self.query.filter(Message.uid == uid).first()
        return msg is not None

    def delete(self, id):
        msg = self.query.filter(Message.id == id).first()

        if msg:
            msg.delete = True

    def undelete(self, id):
        msg = self.query.filter(Message.id == id).first()

        if msg:
            msg.delete = False

    def purge(self, id):
        msg = self.query.filter(Message.id == id).first()

        if msg:
            self.session.delete(msg)

    def add(self, msg):
        self.session.add(msg)

