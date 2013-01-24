# own files
from model import User
from utilities import CryptoUtil
from utilities import constants
from userhandler import perform_login

# libraries
import webapp2
from gaesessions import get_current_session
from google.appengine.api import mail
from i18n_utils import BaseHandler
from base64 import b64encode

class UserRegisterHandler(BaseHandler):
	def get(self):
		session = get_current_session()
		if session.get('email') is not None:
			perform_logout(self, session.get('email'))
		else:
			template = self.jinja2_env.get_template('register.html')
			self.response.out.write(template.render())

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
		user.verified = False
		user.verificationCode = b64encode(CryptoUtil.getVerificationCode(), "*$")
		user.put()

		# Send email for verification
		template_values = {
			'user_email' : self.user_email,
			'code' : user.verificationCode,
			'url' : constants.VERIFICATION_URL
		}
		template = self.jinja2_env.get_template('verificationemail.jinja')
		message = mail.EmailMessage()
		message.sender = constants.SENDER_ADDRESS
		message.to = user.email
		message.subject = 'Please verify your address'
		message.body = template.render(template_values)
		message.send()

		# Log in user
		perform_login(self, user.email)
