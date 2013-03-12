# own modules
from listhandler import ListHandler
from userhandler import UserHandler
from utilities import constants
from user_util import UserUtil

# libraries, builtins
from google.appengine.api import mail
from google.appengine.ext import testbed
import unittest
import webapp2
import webtest
from gaesessions import get_current_session
from webapp2 import Route

class WebTest_List(unittest.TestCase):
	listURL = '/api/v1/Lists'
	
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_mail_stub()
		self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
		app = webapp2.WSGIApplication([
						Route('/<api:api>/v1/Lists/', handler=ListHandler),
						Route('/<api:api>/v1/lists/', handler=ListHandler),
						Route('/<api:api>/v1/Lists', handler=ListHandler),
						Route('/<api:api>/v1/lists', handler=ListHandler),
						Route('/<api:api>/v1/Lists/<list_id>', handler=ListHandler),
						Route('/<api:api>/v1/Lists/<list_id>', handler=ListHandler),
		                Route('/Lists/', handler=ListHandler),
						Route('/lists/', handler=ListHandler),
						Route('/Lists', handler=ListHandler),
						Route('/lists', handler=ListHandler),
						Route('/Lists/<list_id>', handler=ListHandler),
						Route('/lists/<list_id>', handler=ListHandler)
						],
		                              debug=True)
		UserUtil.decorate_app(app)	
		self.testapp = webtest.TestApp(app)
	
	def testWithoutLogin(self):
		response = self.testapp.get(self.listURL, expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED, 'Shopping list queries should not be served without authenticating: ' + str(response.status_int))
		
	def testListOfListsWithLogin(self):
		email = 'james@bond.com'
		password = 'password'
		# 1. Register client
		response = UserUtil.register_user(self.testapp, email, password)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Register failed with correct credentials: ' + str(response.status_int))
		
		# 2. Verify
		response = UserUtil.verify_user(self.testapp, self.mail_stub, email)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: '+ str(response.status_int))

		# Real tests come here
		response = self.testapp.get(self.listURL, expect_errors=True)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Shopping list queries should not be served without authenticating: ' + str(response.status_int))
		
		# 8. Logout
		response = UserUtil.logout(self.testapp)
		self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
		