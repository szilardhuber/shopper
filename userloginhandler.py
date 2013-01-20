# own files
from model import User
from utilities import CryptoUtil
from userhandler import perform_login

# libraries
import webapp2
import os
from google.appengine.ext.webapp import template

class UserLoginHandler(webapp2.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
		self.response.out.write(template.render(path, {}))

	def post(self):
		self.doLogin()
		
	def doLogin(self):
		# Validate email and get user from db
		email = self.request.get('email')
		if not User.isEmailValid(email) or not User.isAlreadyRegistered(email):
			self.error(400)
			return
		user = User.getUser(email);

		# Calculate password hash
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.error(400)
			return
		key = CryptoUtil.getKey(password, user.salt)

		# Validate password
		if not user.password == key:
			self.error(400)
			return
		
		# Log in user
		perform_login(self, user.email)

