from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

class IndexManager(object):
    def __init__(self):
        self.engine = create_engine(config.engine, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
