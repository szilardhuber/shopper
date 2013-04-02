from google.appengine.ext import db
from google.appengine.api import memcache

from listitem import ListItem
from product import Product
from utilities import constants

import logging

class ShoppingList(db.Model):
	name = db.StringProperty()

	NAMESPACE = 'ShoppingList'
	
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
		
	def get_items(self):
		list_items = memcache.get(str(self.key().id_or_name()), namespace = ShoppingList.NAMESPACE)
		if list_items is not None:
			return list_items
		q = ListItem.all()
		q.ancestor(self)
		list_items = q.fetch(1000)
		memcache.add(str(self.key().id_or_name()), list_items, namespace=ShoppingList.NAMESPACE)
		return list_items
		
