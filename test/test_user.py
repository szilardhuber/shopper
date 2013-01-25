from userregisterhandler import UserRegisterHandler
from userloginhandler import UserLoginHandler

import unittest
import webapp2
import webtest

class UserAPICases(unittest.TestCase):
	def setUp(self):
		app = webapp2.WSGIApplication([('/[uU]ser/[lL]ogin', UserLoginHandler),
									('/[uU]ser/[rR]egister', UserRegisterHandler)])
		self.testapp = webtest.TestApp(app)
		
	def testRegisterHandlerEmpty(self):
		response = self.testapp.post('/User/Register', params={}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling without parameters')
		
	def testRegisterHandlerWrongEmail(self):
		response = self.testapp.post('/User/Register', params={'email' : 'jamesbond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email')
		response = self.testapp.post('/User/Register', params={'email' : 'james@com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email')
		response = self.testapp.post('/User/Register', params={'email' : '@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email')
		
	def testRegisterHandlerWeakPassword(self):
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com', 'password' : '1'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with too weak password')
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling without password')
		
	def testRegisterHandlerOK(self):
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials.')
		response = self.testapp.post('/User/Register', params={'email' : 'admin1232431324324@domain1234533334.hu', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials.')
		
	def testRegisteringTwice(self):
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials.')
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Wrong response with correct credentials.')
		
	def testLoginSimple(self):
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Register failed with correct credentials')
		response = self.testapp.post('/User/Login', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Login failed with correct credentials.')

	def testLoginFail(self):
		response = self.testapp.post('/User/Login', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Login succeeded with empty db')
		response = self.testapp.post('/User/Register', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Register failed with correct credentials: ' + str(response.status_int))
		response = self.testapp.post('/User/Login', params={'email' : 'james@bond.com', 'password' : 'password2'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Login succeeded with bad password.')
		response = self.testapp.post('/User/Login', params={'email' : 'james2@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Login succeeded with bad email.')
		
class UserUnitTestCases(unittest.TestCase):
	def testPasswordChecksum(self):
		pass

