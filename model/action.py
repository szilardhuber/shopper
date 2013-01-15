# libraries
from google.appengine.ext import db

class Action(db.Model):
	guid = db.StringProperty()
	barcode = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

