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
	def isValidSession(sessionid):
		return SessionData.get_by_key_name(sessionid, read_policy=db.STRONG_CONSISTENCY)
	
	@staticmethod
	def delete_expired_sessions():
		q = db.Query(SessionData)
		q.filter('startdate <', datetime.now() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES))
		db.delete(q)
		
