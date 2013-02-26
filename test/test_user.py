# own modules
from userhandler import UserHandler
from listproductshandler import ListProductsHandler
from utilities import constants

# libraries, builtins
from google.appengine.api import mail
from google.appengine.ext import testbed
import unittest
import webapp2
import webtest
from gaesessions import get_current_session

class WebTest_User(unittest.TestCase):
	verifyPrefix = 'https://szilardhuber.appspot.com/User/Verify?code='
	loginURL = '/User/Login/API'
	registerURL = '/User/Register/API'
	verifyURL = '/User/Verify'
	logoutURL = '/User/Logout/api'
	
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_mail_stub()
		self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
		app = webapp2.WSGIApplication([
									('/[uU]ser/(.*)/(.*)/', UserHandler),
									('/[uU]ser/(.*)/(.*)', UserHandler),
									('/[uU]ser/(.*)', UserHandler),
									('/(.*)', ListProductsHandler),
									])
		self.testapp = webtest.TestApp(app)
	
	def testRegisterHandlerEmpty(self):
		response = self.__register_user()
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling without parameters: ' + str(response.status_int))
		
	def testRegisterHandlerWrongEmail(self):
		response = self.__register_user('jamesbond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with bad email: ' + str(response.status_int))
		response = self.__register_user('james@com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with bad email: ' + str(response.status_int))
		response = self.__register_user('@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with bad email: ' + str(response.status_int))
		
	def testRegisterHandlerWeakPassword(self):
		response = self.__register_user('james@bond.com', '1')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with too weak password: ' + str(response.status_int))
		response = self.__register_user('james@bond.com')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling without password: ' + str(response.status_int))
		
	def testRegisterHandlerBadPassword(self):
		email = 'james@aisoft.hu'
		password = '"a"@a.hu'
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
		password = 	'"a;"@a.hu'
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
		password = "a'a@a.hu"	
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
		password = "a;a@a.hu"
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
	
	def testRegisterHandlerOK(self):
		response = self.__register_user('james@bond.com','password')
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Wrong response with correct credentials: ' + str(response.status_int))
		response = self.__register_user('admin123254334343434234234@domain12312312434324.hu', 'password')
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Wrong response with correct credentials: ' + str(response.status_int))
		
	def testRegisteringTwice(self):
		response = self.__register_user('james@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Wrong response with correct credentials: ' + str(response.status_int))
		response = self.__register_user('james@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Wrong response for second registration: ' + str(response.status_int))
		response = self.__register_user('jAmes@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'System is case sensitive for emails: ' + str(response.status_int))
		
	def testLoginSuccess(self):
		email = 'james@bond.com'
		password = 'password'
		# 1. Register client
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Access test site - error should arrive
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should be served after logging in: ' + str(response.status_int))

		# 3. Try to login -> Verification needed first
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_FORBIDDEN, 'Server should answer 403 for unverified client: ' +str(response.status_int))

		# 4. Verify
		response = self.__verify_user(email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))
		
		# 5. Access test site should succeed after verification
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))

		# 6. Check login
		session = get_current_session()
		self.assertEqual(session.get(constants.VAR_NAME_EMAIL), email, 'User email is not correct in session variable: ' + str(session.get(constants.VAR_NAME_EMAIL)))
		self.assertIsNotNone(session.get(constants.SESSION_ID), 'SessionId is none')
		
		# 7. Access test site
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))
		
		# 8. Logout
		response = self.testapp.get(self.logoutURL, expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
	def testLoginFailWithoutVerification(self):
		email = 'james@bond.com'
		password = 'password'
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with empty db: ' + str(response.status_int))
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		response = self.__login_user(email, 'password2')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad password: ' + str(response.status_int))
		response = self.__login_user('james2@bond.com', password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad email: ' + str(response.status_int))

	def testLoginFailWithVerification(self):
		email = 'james@bond.com'
		password = 'password'
		
		# 1. Register client
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with empty db: ' + str(response.status_int))
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = self.__verify_user(email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))

		# 3. Logout
		response = self.testapp.get(self.logoutURL, expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))

		# 4. Login with bad credentials
		response = self.__login_user(email, 'password2')		
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad password.')
		response = self.__login_user(email, '')		
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with empty password.')
		response = self.__login_user('james2@bond.com', password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad email.')
		
	def testPersistentCookie(self):
		email = 'jamesbond@aisoft.hu'
		password = '12345678'
		
		# 1. Register client 
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = self.__verify_user(email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))
		
		# 3. Login with remember me turned off
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Login failed with verified client: ' + str(response.status_int))
		
		# 4. Acessing secure content (after login and after deleting session data)
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))
		session = get_current_session()
		session.terminate()
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should not be served without providing session data: ' + str(response.status_int))
		
		# 5. Login with remember me turned on
		response = self.__login_user(email, password, True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Login failed with verified client: ' + str(response.status_int))
		
		# 6. Acessing secure content (after login and after deleting session data)
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))
		session = get_current_session()
		session.terminate()
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))
		
		# Test next login
		session = get_current_session()
		session.terminate()
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))

		# 7. Try to access secure content with modified token
		response = self.testapp.get('/api', expect_errors=True, headers=dict(Cookie='token='))
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))
		
		# 8. Logout
		response = self.testapp.get(self.logoutURL, expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
		# 9. Check logout
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should not be served after logout: ' + str(response.status_int))
		
	def testRegression1(self):
		email = 'regression1@aisoft.hu'
		good_password = '12345678'
		bad_password = 'wronwrongpassword'
		
		# 1. Register client 
		response = self.__register_user(email, good_password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = self.__verify_user(email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))
		
		# 3. Logout client
		response = self.testapp.get(self.logoutURL, expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
		# 4. Check logout
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should not be served after logout: ' + str(response.status_int))

		# 5. Login with remember me turned on and a wrong password
		response = self.__login_user(email, bad_password, True)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad password.' + str(response.status_int))
		
		# 6. Acessing secure content (after login and after deleting session data)
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page must not be served without logging in: ' + str(response.status_int))

	def __register_user(self, email = None, password = None):
		params = {}
		if email is not None:
			params[constants.VAR_NAME_EMAIL] = email
		if password is not None:
			params[constants.VAR_NAME_PASSWORD] = password
		response = self.testapp.post(self.registerURL, params, expect_errors=True)
		return response
	
	def __verify_user(self, email):
		messages = self.mail_stub.get_sent_messages(to=email)
		self.assertEqual(len(messages), 1, "Exactly one message should have been sent to james@bond.com")
		body = messages[0].body.decode()
		url = body[body.find(self.verifyPrefix):]
		code = url[len(self.verifyPrefix):url.find('\n')]
		response = self.testapp.get(self.verifyURL, params={'code' : code}, expect_errors=True)
		return response
	
	def __login_user(self, email, password, remember = False):
		response = self.testapp.post(self.loginURL, params={constants.VAR_NAME_EMAIL : email, constants.VAR_NAME_PASSWORD : password, 'remember' : remember}, expect_errors=True)
		return response

