from userhandler import UserHandler
from listproductshandler import ListProductsHandler

from google.appengine.api import mail
from google.appengine.ext import testbed
import unittest
import webapp2
import webtest
from gaesessions import get_current_session

"""
Tests needed:

 Logout
 
"""

class UserAPICases(unittest.TestCase):
	verifyPrefix = 'https://szilardhuber.appengine.com/User/Verify?code='
	loginURL = '/User/Login/API'
	registerURL = '/User/Register/API'
	verifyURL = '/User/Verify'
	
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
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling without parameters: ' + str(response.status_int))
		
	def testRegisterHandlerWrongEmail(self):
		response = self.__register_user('jamesbond.com', 'password')
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email: ' + str(response.status_int))
		response = self.__register_user('james@com', 'password')
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email: ' + str(response.status_int))
		response = self.__register_user('@bond.com', 'password')
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email: ' + str(response.status_int))
		
	def testRegisterHandlerWeakPassword(self):
		response = self.__register_user('james@bond.com', '1')
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with too weak password: ' + str(response.status_int))
		response = self.__register_user('james@bond.com')
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling without password: ' + str(response.status_int))
		
	def testRegisterHandlerOK(self):
		response = self.__register_user('james@bond.com','password')
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials: ' + str(response.status_int))
		response = self.__register_user('admin123254334343434234234@domain12312312434324.hu', 'password')
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials: ' + str(response.status_int))
		
	def testRegisteringTwice(self):
		response = self.__register_user('james@bond.com', 'password')
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials: ' + str(response.status_int))
		response = self.__register_user('james@bond.com', 'password')
		self.assertEqual(response.status_int, 400, 'Wrong response with correct credentials: ' + str(response.status_int))
		
	def testLoginSuccess(self):
		email = 'james@bond.com'
		password = 'password'
		# 1. Register client
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, 200, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Access test site - error should arrive
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, 401, 'Users only page should be served after logging in: ' + str(response.status_int))

		# 3. Try to login -> Verification needed first
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, 403, 'Server should answer 403 for unverified client: ' +str(response.status_int))

		# 4. Verify
		response = self.__verify_user(email)
		self.assertEqual(response.status_int, 200, 'Verification failed: '+ str(response.status_int))
		
		# 5. Access test site - error should arrive
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, 401, 'Users only page should be served after logging in: ' + str(response.status_int))

		# 6. Login
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, 200, 'Login failed with verified client: ' + str(response.status_int))
		session = get_current_session()
		self.assertEqual(session.get('email'), email, 'User email is not correct in session variable: ' + str(session.get('email')))
		self.assertIsNotNone(session.get('id'), 'SessionId is none')
		
		# 7. Access test site
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Users only page should be served after logging in: ' + str(response.status_int))
		
	def testLoginFailWithoutVerification(self):
		email = 'james@bond.com'
		password = 'password'
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, 400, 'Login succeeded with empty db: ' + str(response.status_int))
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, 200, 'Register failed with correct credentials: ' + str(response.status_int))
		response = self.__login_user(email, 'password2')
		self.assertEqual(response.status_int, 400, 'Login succeeded with bad password: ' + str(response.status_int))
		response = self.__login_user('james2@bond.com', password)
		self.assertEqual(response.status_int, 400, 'Login succeeded with bad email: ' + str(response.status_int))

	def testLoginFailWithVerification(self):
		email = 'james@bond.com'
		password = 'password'
		
		# 1. Register client
		response = self.__login_user(email, password)
		self.assertEqual(response.status_int, 400, 'Login succeeded with empty db: ' + str(response.status_int))
		response = self.__register_user(email, password)
		self.assertEqual(response.status_int, 200, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = self.__verify_user(email)
		self.assertEqual(response.status_int, 200, 'Verification failed: '+ str(response.status_int))

		# 3. Login with bad credentials
		response = self.__login_user(email, 'password2')		
		self.assertEqual(response.status_int, 400, 'Login succeeded with bad password.')
		response = self.__login_user('james2@bond.com', password)
		self.assertEqual(response.status_int, 400, 'Login succeeded with bad email.')	
		
	def __register_user(self, email = None, password = None):
		params = {}
		if email is not None:
			params['email'] = email
		if password is not None:
			params['password'] = password
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
	
	def __login_user(self, email, password):
		response = self.testapp.post(self.loginURL, params={'email' : email, 'password' : password}, expect_errors=True)
		return response
		
class UserUnitTestCases(unittest.TestCase):
	def testPasswordChecksum(self):
		pass

