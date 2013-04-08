from webapp2 import Route
from handlers	 import UserHandler
from utilities import constants

class UserUtil():
	LOGIN_URL = '/User/Login/API'
	REGISTER_URL = '/User/Register/API'
	VERIFY_URL = '/User/Verify'
	LOGOUT_URL = '/User/Logout/api'
	VERIFY_PREFIX = 'https://szilardhuber.appspot.com/User/Verify?code='

	@staticmethod
	def decorate_app(app):
		app.router.add(('/[uU]ser/(.*)/(.*)/', UserHandler))
		app.router.add(('/[uU]ser/(.*)/(.*)', UserHandler))
		app.router.add(('/[uU]ser/(.*)', UserHandler))

	@staticmethod
	def register_user(testapp, email = None, password = None):
		params = {}
		if email is not None:
			params[constants.VAR_NAME_EMAIL] = email
		if password is not None:
			params[constants.VAR_NAME_PASSWORD] = password
		response = testapp.post(UserUtil.REGISTER_URL, params, expect_errors=True)
		return response
	
	@staticmethod
	def verify_user(testapp, mail_stub, email):
		messages = mail_stub.get_sent_messages(to=email)
		body = messages[0].body.decode()
		url = body[body.find(UserUtil.VERIFY_PREFIX):]
		code = url[len(UserUtil.VERIFY_PREFIX):url.find('\n')]
		response = testapp.get(UserUtil.VERIFY_URL, params={'code' : code}, expect_errors=True)
		return response
	
	@staticmethod
	def login_user(testapp, email, password, remember = False):
		response = testapp.post(UserUtil.LOGIN_URL, params={constants.VAR_NAME_EMAIL : email, constants.VAR_NAME_PASSWORD : password, 'remember' : remember}, expect_errors=True)
		return response
	
	@staticmethod
	def logout(testapp):
		response = testapp.get(UserUtil.LOGOUT_URL, expect_errors=True)
		return response
		

