# libraries
from google.appengine.ext import db
from utilities import CryptoUtil
from datetime import datetime, timedelta
from utilities import constants

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
		if sessionid is not None:
			return SessionData.get_by_key_name(sessionid, read_policy=db.STRONG_CONSISTENCY)
		else:
			return None

	@staticmethod
	def isValidSession(sessionid):
		session = SessionData.getSession(sessionid)
		return session is not None
	
	@staticmethod
	def delete_expired_sessions():
		q = db.Query(SessionData)
		q.filter('startdate <', datetime.now() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES))
		db.delete(q)
		
		
