from google.appengine.ext import db
from listitem import ListItem
from product import Product

import logging

class ShoppingList(db.Model):
	name = db.StringProperty()
	
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
	
	def add_item(self, description, quantity):
		q = Product.all()
		q.filter('name = ', description)
		product = q.get()
		q = ListItem.all()
		q.ancestor(self)
		item = None
		if product is not None:
			q.filter('product = ', product)
			item = q.get()
			logging.info('Product: ' +str(product))
			logging.info('Item: ' +str(item))
		else:
			q.filter('description = ', description)
			item = q.get()
			
		if item is None:
			item = ListItem(parent=self)
			item.description = description
			item.quantity = quantity
			item.product = product
			item.put()
		else:
			item.quantity += quantity
			item.put()
		

