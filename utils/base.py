from indexmanager import IndexManager

class BaseUtils(object):
    def __init__(self, session = None):
        if session:
            self.session = session
        else:
            self.session = IndexManager().get_session()

    def close(self):
        if self.session:
            try:
                self.session.commit()
            except:
                self.session.close()

