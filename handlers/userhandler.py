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
from google.appengine.api import memcache


class UserHandler(BaseHandler):
	@viewneeded
	@usercallable
	def get(self, command, api=''):
		if command.lower() == 'logout':
			self.__logout()
			return
		
		if api != '':
			self.error(constants.STATUS_BAD_REQUEST)
			return
		
		if command.lower() in ['login', 'register']:
			if self.user_email is not None:
				self.__display_form('alreadyloggedin.html', self.user_email+'-loggedin')
			else:
				session = get_current_session()
				error_message = session.pop_quick(constants.VAR_NAME_ERRORMESSAGE)
				key = command.lower()
				if error_message is not None:
					key += error_message
				self.__display_form(command.lower() + '.html', key, error_message)
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
			email = self.request.get(constants.VAR_NAME_EMAIL)
			self.__send_verification(email)
			return
			
		self.error(404)
		return

	def __send_verification(self, email):
		user = User.getUser(email)
		if user is None or user.verified:
			self.set_error(constants.STATUS_BAD_REQUEST, message=None, url="/")
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

	def __login(self):
		# Validate email and get user from db
		email = self.request.get(constants.VAR_NAME_EMAIL)
		if not User.isEmailValid(email) or not User.isAlreadyRegistered(email):
			self.set_error(constants.STATUS_BAD_REQUEST, gettext('Incorrect credentials'), url=self.request.url)
			return
		user = User.getUser(email);

		# Calculate password hash
		password = self.request.get(constants.VAR_NAME_PASSWORD)
		if not User.isPasswordValid(password):
			self.set_error(constants.STATUS_BAD_REQUEST, gettext('Incorrect credentials'), url=self.request.url)
			return
		key = CryptoUtil.getKey(password, user.salt)

		# Validate password
		if not user.password == key:
			self.set_error(constants.STATUS_BAD_REQUEST, gettext('Incorrect credentials'), url=self.request.url)
			return
		
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
			self.response.set_cookie(constants.PERSISTENT_LOGIN_NAME, cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=constants.PERSISTENT_LOGIN_LIFETIME_DAYS), path="/", httponly=True, secure=True)
		
		# Log in user
		if user.verified == True:
			user.login(self.request.remote_addr)
			session = get_current_session()
			url = session.pop(constants.VAR_NAME_REDIRECT)
			if url == None:
				url = "/"
			self.ok(url)
		else:
			self.set_error(constants.STATUS_FORBIDDEN, gettext('You have not verified your account yet. Click <a href=\"/User/Verify">here</a> if you have not recieved our email.'), url=self.request.url)
			return
	
	def __logout(self):
		if constants.PERSISTENT_LOGIN_NAME in self.request.cookies:
			token = LoginToken.get(self.request.cookies[constants.PERSISTENT_LOGIN_NAME])
			if token is not None:
				token.delete()
		self.response.delete_cookie(constants.PERSISTENT_LOGIN_NAME, '/')
		user = User.getUser(self.user_email)
		if user is not None:
			user.logout()
		self.ok('/')
		
	def __register(self):
		# Validate email
		email = self.request.get(constants.VAR_NAME_EMAIL)
		if not User.isEmailValid(email) or User.isAlreadyRegistered(email):
			self.set_error(constants.STATUS_BAD_REQUEST, gettext('Incorrect credentials'), url=self.request.url)
			return
			
		# Validate password
		password = self.request.get(constants.VAR_NAME_PASSWORD)
		if not User.isPasswordValid(password):
			self.set_error(constants.STATUS_BAD_REQUEST, gettext('Incorrect credentials'), url=self.request.url)
			return
			
		# Calculate password hash
		salt_and_key = CryptoUtil.get_salt_and_key(password)
		salt = salt_and_key[0]
		key = salt_and_key[1]
		
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
	
		
	def __display_form(self, template, key, error_message = None):
		page = memcache.get(key, namespace='Pages')
		if page is None:
			template_values = {
				'user_email' : self.user_email,
				constants.VAR_NAME_ERRORMESSAGE : error_message
			}
			template = self.jinja2_env.get_template(template)
			page = template.render(template_values)
			memcache.add(key, page, namespace='Pages')
		self.response.out.write(page)