from google.appengine.ext import db

class Action(db.Model):
	#guid = db.StringProperty()
	barcode = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

def user_key(user_guid=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('User', user_guid or 'default_user')

