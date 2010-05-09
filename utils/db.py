from indexmanager import IndexManager
from model import Base
from . import BaseUtils

class DBUtils(BaseUtils):
    @classmethod
    def create(self):
        Base.metadata.create_all(IndexManager().engine)

    @classmethod
    def drop(self):
        Base.metadata.drop_all(IndexManager().engine)

    def truncate(self, table):
        if table.__table__.exists(self.session.bind):
            self.session.connection().execute(table.__table__.delete())

