# own files
from model import User
from utilities import CryptoUtil
from userhandler import perform_login
from userhandler import perform_logout

# libraries
import webapp2
from gaesessions import get_current_session

from i18n_utils import BaseHandler

class UserLoginHandler(BaseHandler):
	def get(self):
		session = get_current_session()
		if session.get('email') is not None:
			perform_logout(self, session.get('email'))
		else:
			template = self.jinja2_env.get_template('login.html')
			self.response.out.write(template.render())

	def post(self):
		self.doLogin()
		
	def doLogin(self):
		# Validate email and get user from db
		email = self.request.get('email')
		if not User.isEmailValid(email) or not User.isAlreadyRegistered(email):
			self.error(401)
			return
		user = User.getUser(email);

		# Calculate password hash
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.error(401)
			return
		key = CryptoUtil.getKey(password, user.salt)

		# Validate password
		if not user.password == key:
			self.error(401)
			return
		
		# Log in user
		if user.verified:
			perform_login(self, user.email)
		else:
			pass # navigate to send again URL

