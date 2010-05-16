from utils.base import BaseUtils
from model import Recipient

class RecipientUtils(BaseUtils):
    def get_recipients(self):
        results = []

        query = self.session.query(Recipient)

        for recipient in query.all():
            results.append(recipient)

        return results


    def lookup_recipient(self, display, mail, create):
        query = self.session.query(Recipient)

        recipient = query.filter(Recipient.mail == mail).first()
        if recipient is None and create:
            recipient = Recipient(display, mail)
            self.session.add(recipient)

        return recipient
