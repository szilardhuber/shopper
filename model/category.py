# libraries
from google.appengine.ext import db

class Category(db.Model):
	description = db.StringProperty()
	
	

