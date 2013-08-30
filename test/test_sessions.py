""" Unit and functional tests for list handler """
from handlers import SessionHandler
from utilities import constants

# libraries, builtins
from google.appengine.ext import testbed
import unittest
import webapp2
import webtest
from webapp2 import Route
from gaesessions import Session, set_current_session, get_current_session


class WebTest_List(unittest.TestCase):
    request_token_url = '/api/v2/sessions/new'

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        set_current_session(Session())
        self.testbed.init_mail_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        app = webapp2.WSGIApplication([
            Route('/api/v<api_version>/sessions<:/?>', handler=SessionHandler),
            Route('/api/v<api_version>/sessions/<new:new>', handler=SessionHandler)
        ],
            debug=True)
        self.testapp = webtest.TestApp(app)

    def test_request_token_bad_url(self):
        """ Tests REQUEST TOKEN API METHOD with bad calling """
        response = self.testapp.get('/api/v1/sessions/new', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with api version "1": ' + str(response.status_int))
        response = self.testapp.get('/api/va/sessions/new', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with api version "a": ' + str(response.status_int))
        response = self.testapp.get('/api/v2.5/sessions/new', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with api version "2.5": ' + str(response.status_int))
        response = self.testapp.get('/api/v/sessions/new', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_NOT_FOUND,
                         'Request should fail with api version "": ' + str(response.status_int))
        response = self.testapp.get('/api/v2/sessions/now', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_NOT_FOUND,
                         'Request should fail with "now" as "new" value: ' + str(response.status_int))
        
    def test_request_token_bad_params(self):
        """ Tests REQUEST TOKEN API METHOD with bad parameters """
        response = self.testapp.get(self.request_token_url, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with no email parameter: ' + str(response.status_int))

        response = self.testapp.get(self.request_token_url + '?email=', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with empty email parameter: ' + str(response.status_int))

        response = self.testapp.get(self.request_token_url + '?email=a', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with bad email parameter: "a"' + str(response.status_int))

        response = self.testapp.get(self.request_token_url + '?email=james@', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with bad email parameter: "james@"' + str(response.status_int))

        response = self.testapp.get(self.request_token_url + '?email=james@bond', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with bad email parameter: "james@bond"' + str(response.status_int))

        response = self.testapp.get(self.request_token_url + '?email=james@bond.c', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Request should fail with bad email parameter: "james@bond.c"' + str(response.status_int))

    def test_request_token_ok(self):
        """ Tests REQUEST TOKEN API METHOD with good calling and parameters """
        # 1. Check for one request, valid token should come back
        email = 'james@bond.com'
        response = self.testapp.get(self.request_token_url + '?email=' + email, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK,
                        'Request should succeed with good calling and parameters: ' + str(response.status_int))
        session = get_current_session()
        token = session.get(email)
        self.assertNotEqual('', token)
        self.assertNotEqual(0, token)
        self.assertIsNotNone(token)

        # 2. Check for an other email address, also valid but different token should come back
        email2 = 'james2@bond.com'
        response = self.testapp.get(self.request_token_url + '?email=' + email2, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK,
                        'Request should succeed with good calling and parameters: ' + str(response.status_int))
        session = get_current_session()
        token2 = session.get(email2)
        self.assertNotEqual('', token2)
        self.assertNotEqual(0, token2)
        self.assertIsNotNone(token2)
        self.assertNotEqual(token, token2)

