# libraries
from google.appengine.ext import db
from utilities import CryptoUtil
from datetime import datetime, timedelta
from utilities import constants
import logging
from google.appengine.api import memcache

class SessionData(db.Model):
	email = db.EmailProperty()
	sessionid = db.ByteStringProperty()
	startdate = db.DateTimeProperty(auto_now_add=True)
	ip = db.StringProperty()

	@staticmethod
	def generateId():
		return ''.join('%02x' % ord(byte) for byte in CryptoUtil.getSessionId())

	@staticmethod
	def getSession(sessionid):
		if sessionid is None:
			return None
		session = memcache.get(sessionid, namespace='Session')
		if session is not None:
			return session
		else:
			session = SessionData.get_by_key_name(sessionid, read_policy=db.STRONG_CONSISTENCY)
			memcache.add(sessionid, session, time=36000, namespace='Session')
			return session

	@staticmethod
	def delete_expired_sessions():
		q = db.Query(SessionData)
		q.filter('startdate <', datetime.now() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES))
		db.delete(q)
		
	def isValid(self):
		return self.startdate > datetime.now() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES)
	
	def update_startdate(self):
		self.startdate = datetime.now()
		memcache.set(self.sessionid, self, time=36000, namespace='Session')
