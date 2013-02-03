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
	def verify(code):
		q = db.Query(User)
		q.filter('verificationCode =', code)
		if q.count() == 1:
			verifiedUser = q.get()
			verifiedUser.verified = True
			verifiedUser.verificationCode = None
			verifiedUser.put()
			return True
		else:
			return False

