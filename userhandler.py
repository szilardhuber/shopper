from model.sessiondata import SessionData
from model import User
from model import LoginToken
from utilities import CryptoUtil
from utilities import constants
from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler

# External libraries
from gaesessions import get_current_session
from base64 import b64encode
from google.appengine.api import mail
import logging
import datetime


class UserHandler(BaseHandler):
	@viewneeded
	@usercallable
	def get(self, command, api=''):
		if command.lower() == 'logout':
			self.__logout()
			return
		
		if api != '':
			self.error(400)
			return
		
		if command.lower() in ['login', 'register']:
			session = get_current_session()
			if session.get('email') is not None:
				self.__display_form('alreadyloggedin.html')
			else:
				self.__display_form(command.lower() + '.html')
			return
		
		if command.lower() == 'verify':
			self.__verify()
			return
		
		self.error(404)
		return

	@viewneeded
	def post(self, command, api=''):
		if api != '' and api.lower() != 'api':
			self.error(404)
			return
		
		if command.lower() == 'login':
			self.__login()
			return
			
		if command.lower() == 'register':
			self.__register()
			return
		
		if command.lower() == 'verify' and api == '':
			email = self.request.get('email')
			self.__send_verification(email)
			return
			
		self.error(404)
		return

	def __send_verification(self, email):
		user = User.getUser(email)
		if user is None or user.verified:
			self.set_error(400, message=None, url="/")
			return
		user.verificationCode = b64encode(CryptoUtil.getVerificationCode(), "*$")
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
		user.put()
		self.ok('/')

	def __logout(self):
		self.response.delete_cookie('token', '/')
		session = get_current_session()
		if session.get('email') is None:
			return
		sessionid = session.get(constants.SESSION_ID)
		sessionData = SessionData.getSession(sessionid)
		if sessionData is not None:
			sessionData.delete()
		session.terminate()
		self.ok('/')

	def __login(self):
		# Validate email and get user from db
		email = self.request.get('email')
		if not User.isEmailValid(email) or not User.isAlreadyRegistered(email):
			self.set_error(400, gettext('Incorrect credentials'), url=self.request.url)
			return
		user = User.getUser(email);

		# Calculate password hash
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.set_error(400, gettext('Incorrect credentials'), url=self.request.url)
			return
		key = CryptoUtil.getKey(password, user.salt)

		# Check remember me
		rememberString = self.request.get('remember').lower()
		remember = rememberString != '' and rememberString != 'false'
		if remember:
			token_id = LoginToken.generateId()
			token = LoginToken()
			token.tokenid = token_id
			token.ip = self.request.remote_addr
			token.user = email
			token.put()
			cookie_value = token.get_cookie_value()
			self.response.set_cookie('token', cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=constants.PERSISTENT_LOGIN_LIFETIME_DAYS), path="/", httponly=True, secure=True)
		
		# Validate password
		if not user.password == key:
			self.set_error(400, gettext('Incorrect credentials'), url=self.request.url)
			return
		
		# Log in user
		if user.verified == True:
			user.login(self.request.remote_addr)
			session = get_current_session()
			url = session.pop('returnurl')
			if url == None:
				url = "/"
			self.ok(url)
		else:
			self.set_error(403, gettext('You have not verified your account yet. Click <a href=\"/User/Verify">here</a> if you have not recieved our email.'), url=self.request.url)
			return
		
	def __register(self):
		# Validate email
		email = self.request.get('email')
		if not User.isEmailValid(email) or User.isAlreadyRegistered(email):
			self.set_error(400, gettext('Incorrect credentials'), url=self.request.url)
			return
			
		# Validate password
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.set_error(400, gettext('Incorrect credentials'), url=self.request.url)
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
		user.put()

		# Send email for verification
		self.__send_verification(email)

		self.ok()
		
	
	def __verify(self):
		send = False
		error = False
		code = self.request.get('code')
		if code is None or code == '':
			send = True
		else:
			email = User.verify(code, self.request.remote_addr)
			if email is not None:
				self.user_email = email
			else:
				send = True
				error = True
				
		template_values = {
			'user_email' : self.user_email,
			'send' : send,
			'error' : error
		}
		template = self.jinja2_env.get_template('verification.html')
		self.response.out.write(template.render(template_values))
	
		
	def __display_form(self, template):
		session = get_current_session()
		errorMessage = session.pop_quick('errormessage')
		template_values = {
			'user_email' : self.user_email,
			'errormessage' : errorMessage
		}
		template = self.jinja2_env.get_template(template)
		self.response.out.write(template.render(template_values))