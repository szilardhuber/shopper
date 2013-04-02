# libraries
from google.appengine.ext import db

class Manufacturer(db.Model):
	name = db.StringProperty()

	def to_dict(self):
		ret = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
		return ret
	
	

