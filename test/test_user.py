# own modules
from userhandler import UserHandler
from listproductshandler import ListProductsHandler
from utilities import constants
from user_util import UserUtil

# libraries, builtins
from google.appengine.api import mail
from google.appengine.ext import testbed
import unittest
import webapp2
import webtest
from gaesessions import get_current_session

class WebTest_User(unittest.TestCase):
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
		response = UserUtil.register_user(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling without parameters: ' + str(response.status_int))
		
	def testRegisterHandlerWrongEmail(self):
		response = UserUtil.register_user(self.testapp, 'jamesbond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with bad email: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, 'james@com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with bad email: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, '@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with bad email: ' + str(response.status_int))
		
	def testRegisterHandlerWeakPassword(self):
		response = UserUtil.register_user(self.testapp, 'james@bond.com', '1')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with too weak password: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, 'james@bond.com')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling without password: ' + str(response.status_int))
		
	def testRegisterHandlerBadPassword(self):
		email = 'james@aisoft.hu'
		password = '"a"@a.hu'
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
		password = 	'"a;"@a.hu'
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
		password = "a'a@a.hu"	
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
		password = "a;a@a.hu"
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Code constants.STATUS_BAD_REQUEST should arrive when calling with invalid characters in password: ' + password + ' ' + str(response.status_int))
	
	def testRegisterHandlerOK(self):
		response = UserUtil.register_user(self.testapp, 'james@bond.com','password')
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Wrong response with correct credentials: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, 'admin123254334343434234234@domain12312312434324.hu', 'password')
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Wrong response with correct credentials: ' + str(response.status_int))
		
	def testRegisteringTwice(self):
		response = UserUtil.register_user(self.testapp, 'james@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Wrong response with correct credentials: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, 'james@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Wrong response for second registration: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, 'jAmes@bond.com', 'password')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'System is case sensitive for emails: ' + str(response.status_int))
		
	def testLoginSuccess(self):
		email = 'james@bond.com'
		password = 'password'
		# 1. Register client
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Access test site - error should arrive
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should be served after logging in: ' + str(response.status_int))

		# 3. Try to login -> Verification needed first
		response = UserUtil.login_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_FORBIDDEN, 'Server should answer 403 for unverified client: ' +str(response.status_int))

		# 4. Verify
		response = UserUtil.verify_user(self.testapp, self.mail_stub, email)
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
		response = UserUtil.logout(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
		# 9. SH-26 regression
		response = UserUtil.logout(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
	def testLoginFailWithoutVerification(self):
		email = 'james@bond.com'
		password = 'password'
		response = UserUtil.login_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with empty db: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		response = UserUtil.login_user(self.testapp, email, 'password2')
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad password: ' + str(response.status_int))
		response = UserUtil.login_user(self.testapp, 'james2@bond.com', password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad email: ' + str(response.status_int))

	def testLoginFailWithVerification(self):
		email = 'james@bond.com'
		password = 'password'
		
		# 1. Register client
		response = UserUtil.login_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with empty db: ' + str(response.status_int))
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = UserUtil.verify_user(self.testapp, self.mail_stub, email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))

		# 3. Logout
		response = UserUtil.logout(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))

		# 4. Login with bad credentials
		response = UserUtil.login_user(self.testapp, email, 'password2')		
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad password.')
		response = UserUtil.login_user(self.testapp, email, '')		
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with empty password.')
		response = UserUtil.login_user(self.testapp, 'james2@bond.com', password)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad email.')
		
	def testPersistentCookie(self):
		email = 'jamesbond@aisoft.hu'
		password = '12345678'
		
		# 1. Register client 
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = UserUtil.verify_user(self.testapp, self.mail_stub, email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))
		
		# 3. Login with remember me turned off
		response = UserUtil.login_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Login failed with verified client: ' + str(response.status_int))
		
		# 4. Acessing secure content (after login and after deleting session data)
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Users only page should be served after logging in: ' + str(response.status_int))
		session = get_current_session()
		session.terminate()
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should not be served without providing session data: ' + str(response.status_int))
		
		# 5. Login with remember me turned on
		response = UserUtil.login_user(self.testapp, email, password, True)
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
		response = UserUtil.logout(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
		# 9. Check logout
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should not be served after logout: ' + str(response.status_int))
		
	def testRegression1(self):
		email = 'regression1@aisoft.hu'
		good_password = '12345678'
		bad_password = 'wronwrongpassword'
		
		# 1. Register client 
		response = UserUtil.register_user(self.testapp, email, good_password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify client
		response = UserUtil.verify_user(self.testapp, self.mail_stub, email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))
		
		# 3. Logout client
		response = UserUtil.logout(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		
		# 4. Check logout
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page should not be served after logout: ' + str(response.status_int))

		# 5. Login with remember me turned on and a wrong password
		response = UserUtil.login_user(self.testapp, email, bad_password, True)
		self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Login succeeded with bad password.' + str(response.status_int))
		
		# 6. Acessing secure content (after login and after deleting session data)
		response = self.testapp.get('/api', expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Users only page must not be served without logging in: ' + str(response.status_int))
