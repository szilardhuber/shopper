from google.appengine.ext import db

class List(db.Model):
	name = db.StringProperty()
	
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
