from model.sessiondata import SessionData
from model import User
from utilities import CryptoUtil
from utilities import constants
from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler

# External libraries
from gaesessions import get_current_session
from base64 import b64encode
from google.appengine.api import mail


class UserHandler(BaseHandler):
	@viewneeded
	@usercallable
	def get(self, command, api = ''):
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
	def post(self, command, api = ''):
		if api != '' and api.lower() != 'api':
			self.error(404)
			return
		
		if command.lower() == 'login':
			self.__login()
			return
			
		if command.lower() == 'register':
			self.__register()
			return
			
		self.error(404)
		return

	def __logout(self):
		session = get_current_session()
		if session.get('email') is None:
			return
		sessionid = session.get('id')
		sessionData = SessionData.getSession(sessionid)
		if sessionData is not None:
			sessionData.delete()
		session['id'] = None
		session['email'] = None
		self.ok('/')

	def __login(self):
		# Validate email and get user from db
		email = self.request.get('email')
		if not User.isEmailValid(email) or not User.isAlreadyRegistered(email):
			self.set_error(400, gettext('Incorrect credentials'))
			return
		user = User.getUser(email);

		# Calculate password hash
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.set_error(400, gettext('Incorrect credentials'))
			return
		key = CryptoUtil.getKey(password, user.salt)

		# Validate password
		if not user.password == key:
			self.set_error(400, gettext('Incorrect credentials'))
			return
		
		# Log in user
		if user.verified:
			self.__perform_login(user.email)
			session = get_current_session()
			self.ok(session.pop('returnurl'))
		else:
			self.set_error(403)
			return
		
	def __register(self):
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

		self.response.out.write(user.verificationCode)
		
	
	def __verify(self):	
		code = self.request.get('code')
		if code is None or code == '':
			self.error(400)
		else:
			success = User.verify(code)
			if success:
				template = self.jinja2_env.get_template('verification.html')
				self.response.out.write(template.render())
			else:
				self.error(400)	
		
	def __display_form(self, template):
		session = get_current_session()
		errorMessage = session.pop_quick('errormessage')
		template_values = {
			'user_email' : self.user_email,
			'errormessage' : errorMessage
		}
		template = self.jinja2_env.get_template(template)
		self.response.out.write(template.render(template_values))
			
	def __perform_login(self, email):
		sessionid = SessionData.generateId()
		sessionData = SessionData(key_name=sessionid)
		sessionData.sessionid = sessionid
		sessionData.email = email
		sessionData.ip = self.request.remote_addr
		sessionData.put()
		session = get_current_session()
		session['id'] = sessionid
		session['email'] = email