# own files
from model import User
from utilities import CryptoUtil
from userhandler import perform_login

# libraries
import webapp2
import os
from google.appengine.ext.webapp import template

class UserRegisterHandler(webapp2.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/register.html')
		self.response.out.write(template.render(path, {}))

	def post(self):
		self.doRegister()
		
	def doRegister(self):
		# Validate email
		email = self.request.get('email')
		if not User.isEmailValid(email) or User.isAlreadyRegistered(email):
			self.error(400)
			return
			
		# Validate password
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.response.out.write('Invalid arguments<br>')
			self.error(400)
			return
			
		# Calculate password hash
		r = CryptoUtil.getKeyAndSalt(password)
		salt = r['salt']
		key = r['key']
		
		# Create and store user object
		user = User(key_name=email)
		user.email = email
		user.salt = salt
		user.password = key
		user.put()

		# Log in user
		perform_login(self, user.email)
