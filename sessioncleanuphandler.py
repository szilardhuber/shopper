# own files
from gaesessions import delete_expired_sessions
from model.sessiondata import SessionData

# libraries
from google.appengine.ext import db
import webapp2

class SessionCleanupHandler(webapp2.RequestHandler):
	def get(self):
		finished = False
		# while is needed as this geasessions function only deletes 500 sessions at a time
		while not finished:
			finished = delete_expired_sessions()
		SessionData.delete_expired_sessions()
		
