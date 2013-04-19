""" Contains ListItem model class """
from google.appengine.ext import db
from model.product import Product


class ListItem(db.Model):
    """ ListItem model class """
    product = db.ReferenceProperty(Product)
    description = db.StringProperty()
    quantity = db.IntegerProperty()

    def to_dict(self):
        """ For JSON serialization """
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties() if p != 'product'])
        if self.product is not None:
            ret['product'] = self.product.to_dict()
        ret['id'] = self.key().id_or_name()
        return ret
