from . import BaseUtils
from model import Tag

class TagUtils(BaseUtils):
    def get_tags(self):
        results = []

        query = self.session.query(Tag)
        
        for tag in query.all():
            results.append(tag)
        
        return results

    def get_byname(tagname, create = False):
        query = session.query(Tag)

        tag = query.filter(Tag.name == tagname).first()
        if tag is None and create:
            tag = Tag(tagname)
            session.add(tag)

        return tag 

