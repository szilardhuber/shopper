from google.appengine.ext import db
from product import Product

class ListItem(db.Model):
	product = db.ReferenceProperty(Product)
	description = db.StringProperty()
	quantity = db.IntegerProperty()
	
	def to_dict(self):
		ret = dict([(p, unicode(getattr(self, p))) for p in self.properties() if p != 'product'])
		if self.product is not None:
			ret['product'] = self.product.to_dict() 
		return ret
