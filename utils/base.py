import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

class BaseUtils(object):
    def __init__(self, session = None):
        if session:
            self.session = session
        else:
            engine = create_engine(config.engine)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def close(self):
        if self.session:
            try:
                self.session.commit()
            except:
                self.session.close()

