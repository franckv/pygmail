from . import BaseUtils, TagUtils
from model import Thread

class ThreadUtils(BaseUtils):
    def add_tag(self, id, tagname):
        tagutils = TagUtils(self.session)
        tag = tagutils.get_byname(tagname, True)

        query = session.query(Thread)
        thread = query.filter(Thread.id == id).first()
        
        thread.tags.append(tag)
