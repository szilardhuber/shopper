# own modules
from utilities import CryptoUtil
from utilities import constants

# libraries, builtins
from datetime import datetime, timedelta
from google.appengine.ext import db
from google.appengine.api import memcache

class SessionData(db.Model):
	'''
	Model object representing user sessions. The session is a limited time period until that we consider the user to be logged in.
	'''
	
	NAMESPACE='Session'
	
	email = db.EmailProperty()
	sessionid = db.ByteStringProperty()
	startdate = db.DateTimeProperty(auto_now_add=True)
	ip = db.StringProperty()

	@staticmethod
	def generateId():
		'''
		Generates the sessionid user for authentication during the lifetime of the session. The output is hex_encoded
		'''
		return ''.join('%02x' % ord(byte) for byte in CryptoUtil.getSessionId())

	@staticmethod
	def getSession(sessionid):
		'''
		Retrieves the session from the DB for the given id.
		:param sessionid:
		'''
		if sessionid is None:
			return None
		session = memcache.get(sessionid, namespace=SessionData.NAMESPACE)
		if session is not None:
			return session
		else:
			session = SessionData.get_by_key_name(sessionid, read_policy=db.STRONG_CONSISTENCY)
			if session is not None:
				memcache.add(sessionid, session, time=36000, namespace=SessionData.NAMESPACE)
			return session

	def delete(self):
		'''
		Override base function. Deletes value also from cache.
		'''
		memcache.delete(self.sessionid, namespace=SessionData.NAMESPACE)
		db.Model.delete(self)

	@staticmethod
	def delete_expired_sessions():
		'''
		Delete old sessions from datastore
		'''
		q = db.Query(SessionData)
		q.filter('startdate <', datetime.now() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES))
		db.delete(q)
		
	def isValid(self):
		'''
		Returns False is a session is too old
		'''
		return self.startdate > datetime.now() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES)
	
	def update_startdate(self):
		'''
		We should update the startdate every time the user does something on the site
		'''
		self.startdate = datetime.now()
		memcache.set(self.sessionid, self, time=36000, namespace=SessionData.NAMESPACE)
