""" Contains ListItem model class """
from google.appengine.ext import db


class ListItem(db.Model):
    """ ListItem model class """
    product_barcode = db.StringProperty()
    description = db.StringProperty()
    quantity = db.IntegerProperty()

    def to_dict(self):
        """ For JSON serialization """
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        ret['id'] = self.key().id_or_name()
        return ret
