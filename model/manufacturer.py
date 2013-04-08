""" Contains Manufacturer class """
from google.appengine.ext import db


class Manufacturer(db.Model):
    """ Model class for Manufacturer """
    name = db.StringProperty()

    def to_dict(self):
        """ For JSON serialization """
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        return ret
