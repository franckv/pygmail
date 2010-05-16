from model import Message
from utils import BaseUtils

class MessageUtils(BaseUtils):
    def get_ids(self):
        results = []

        query = self.session.query(Message)

        for msg in query.all():
            results.append(msg.id)

        return results

    def get(self, id):
        query = self.session.query(Message)
        msg = query.filter(Message.id == id).first()
        return msg

    def get_messages(self, limit = 10):
        results = []

        query = self.session.query(Message).limit(limit)

        for msg in query.all():
            results.append(msg)

        return results

    def exists(self, uid):
        query = self.session.query(Message)
        msg = query.filter(Message.uid == uid).first()
        return msg is not None

    def delete(self, id):
        query = self.session.query(Message)
        msg = query.filter(Message.id == id).first()

        if msg:
            self.session.delete(msg)

    def add(self, msg):
        self.session.add(msg)

