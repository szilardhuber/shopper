from google.appengine.ext import db
from product import Product

class ListItem(db.Model):
	product = db.ReferenceProperty(Product)
	description = db.StringProperty()
	quantity = db.IntegerProperty()