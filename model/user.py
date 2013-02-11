from sessiondata import SessionData
from utilities import constants
from gaesessions import get_current_session

# libraries
from google.appengine.ext import db
from django.core.validators import email_re
import re

class User(db.Model):
	email = db.EmailProperty()
	salt = db.ByteStringProperty()
	password = db.ByteStringProperty()
	registrationdate = db.DateTimeProperty(auto_now_add=True)
	verified = db.BooleanProperty()
	verificationCode = db.ByteStringProperty()
	
	@staticmethod
	def getUser(email):
		return User.get_by_key_name(email, read_policy=db.STRONG_CONSISTENCY)
	
	@staticmethod
	def isAlreadyRegistered(email):
		current = User.getUser(email)
		if current is None:
			return False
		else:
			return True
			
	@staticmethod
	def isEmailValid(email):
		if not email_re.match(email):
			return False
		return True
		
	@staticmethod
	def isPasswordValid(password):
		if password is None:
			return False
		if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
			return False
		return True

	@staticmethod
	def verify(code, ip):
		q = db.Query(User)
		q.filter('verificationCode =', code)
		if q.count() == 1:
			verifiedUser = q.get()
			verifiedUser.verified = True
			verifiedUser.verificationCode = None
			verifiedUser.put()
			verifiedUser.login(ip)
			return verifiedUser.email
		else:
			return None

	def	login(self, ip):
		sessionid = SessionData.generateId()
		sessionData = SessionData(key_name=sessionid)
		sessionData.sessionid = sessionid
		sessionData.email = self.email
		sessionData.ip = ip
		sessionData.put()
		session = get_current_session()
		session[constants.SESSION_ID] = sessionid
		session['email'] = self.email
		
	def logout(self):
		session = get_current_session()
		if session.get('email') is None:
			return
		sessionid = session.get(constants.SESSION_ID)
		sessionData = SessionData.getSession(sessionid)
		if sessionData is not None:
			sessionData.delete()
		session.terminate()
