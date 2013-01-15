from userregisterhandler import UserRegisterHandler

import unittest
import webapp2
import webtest

class UserAPICases(unittest.TestCase):
	def setUp(self):
		pass
		app = webapp2.WSGIApplication([('/', UserRegisterHandler)])
		self.testapp = webtest.TestApp(app)
		
	def testRegisterHandlerEmpty(self):
		response = self.testapp.post('/', params={}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling without parameters')
		
	def testRegisterHandlerWrongEmail(self):
		response = self.testapp.post('/', params={'email' : 'jamesbond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email')
		response = self.testapp.post('/', params={'email' : 'james@com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email')
		response = self.testapp.post('/', params={'email' : '@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with bad email')
		
	def testRegisterHandlerWeakPassword(self):
		response = self.testapp.post('/', params={'email' : 'james@bond.com', 'password' : '1'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling with too weak password')
		response = self.testapp.post('/', params={'email' : 'james@bond.com'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Code 400 should arrive when calling without password')
		
	def testRegisterHandlerOK(self):
		response = self.testapp.post('/', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials.')
		response = self.testapp.post('/', params={'email' : 'admin1232431324324@domain1234533334.hu', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials.')
		
	def testRegisteringTwice(self):
		response = self.testapp.post('/', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 200, 'Wrong response with correct credentials.')
		response = self.testapp.post('/', params={'email' : 'james@bond.com', 'password' : 'password'}, expect_errors=True)
		self.assertEqual(response.status_int, 400, 'Wrong response with correct credentials.')
		
class UserUnitTestCases(unittest.TestCase):
	def testPasswordChecksum(self):
		pass

