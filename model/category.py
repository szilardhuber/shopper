""" Contains category model class """
from google.appengine.ext import db


class Category(db.Model):
    """ Category model class """
    description = db.StringProperty()

    def to_dict(self):
        """ For JSON serialization """
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        return ret
