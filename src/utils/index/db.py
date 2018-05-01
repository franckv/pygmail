from model import Base
from . import BaseUtils

class DBUtils(BaseUtils):
    def create(self):
        Base.metadata.create_all(self.session.bind)

    def drop(self):
        Base.metadata.drop_all(self.session.bind)

    def truncate(self, table):
        if table.__table__.exists(self.session.bind):
            self.session.connection().execute(table.__table__.delete())

