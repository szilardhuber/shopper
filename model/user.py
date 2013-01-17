# libraries
from google.appengine.ext import db
from django.core.validators import email_re

class User(db.Model):
	email = db.EmailProperty()
	salt = db.ByteStringProperty()
	password = db.ByteStringProperty()
	registrationdate = db.DateTimeProperty(auto_now_add=True)
	
	@staticmethod
	def isAlreadyRegistered(email):
		current = User.get_by_key_name(email, read_policy=db.STRONG_CONSISTENCY)
		if current is None:
			return False
		else:
			return True
			
	@staticmethod
	def isEmailValid(email):
		if not email_re.match(email):
			return False
		if User.isAlreadyRegistered(email):
			return False
		return True
		
	@staticmethod
	def isPasswordValid(password):
		if password is None:
			return False
		if password == '': #what if '    '? I suggest trim. What if password contains any other whitespace char? Use regex instead of.
			return False
		if len(password) < 8: # regex can check this as well.
			return False
		return True


