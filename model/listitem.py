from google.appengine.ext import db

class ListItem(db.Model):
	barcode = db.StringProperty()
	description = db.StringProperty()
	quantity = db.IntegerProperty()