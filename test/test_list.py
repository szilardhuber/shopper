# own modules
from handlers import ListHandler
from handlers import UserHandler
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
from gaesessions import Session, set_current_session


class WebTest_List(unittest.TestCase):
    listURL = '/api/v1/Lists'

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        set_current_session(Session())
        self.testbed.init_mail_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
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

    def test_without_login(self):
        """ Test all list API function without login. They should fail """

        # List shopping lists
        response = self.testapp.get(self.listURL, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED,
                         'Shopping list queries should not be served without authenticating: ' + str(response.status_int))
        # Create shopping list
        response = self.testapp.post(self.listURL, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_UNAUTHORIZED,
                         'Shopping list queries should not be served without authenticating: ' + str(response.status_int))

    def test_list_with_login(self):
        """ Test listing of shopping lists """
        self.__login__()

        # Test empty list
        response = self.testapp.get(self.listURL, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK,
                         'Shopping list queries should be served after authentication: ' + str(response.status_int))
        self.assertEqual(response.json, [], 'There should not be a shopping list here.')

        # Create list
        list_name = 'Test_list_api'
        response = self.testapp.post(self.listURL, {'name': list_name}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK,
                         'Creating shopping list failed: ' + str(response.status_int))

        # Check creation
        response = self.testapp.get(self.listURL, expect_errors=True)
        self.assertEqual(len(response.json), 1,
                         'Number of lists does not match: ' + str(len(response.json)))
        self.assertEqual(response.json[0]['name'], list_name,
                         'Creating shopping list failed: ' + str(response.status_int))

        # Creating with empty name parameter
        response = self.testapp.post(self.listURL, {'name': ''}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Creating new list with empty name given should have failed: ' + str(response.status_int))

        # Creating without name parameter
        response = self.testapp.post(self.listURL, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Creating new list without name given should have failed: ' + str(response.status_int))

        # Creating again with same name
        response = self.testapp.post(self.listURL, {'name': list_name}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Creating new list with same name should have failed: ' + str(response.status_int))

        # Create second
        list_name_second = 'Test_list_api_2'
        response = self.testapp.post(self.listURL, {'name': list_name_second}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK,
                         'Creating shopping list failed: ' + str(response.status_int))
        # Check creation of second
        response = self.testapp.get(self.listURL, expect_errors=True)
        self.assertEqual(len(response.json), 2,
                         'Number of lists does not match: ' + str(len(response.json)))
        self.assertEqual(response.json[0]['name'], list_name,
                         'Creating shopping list failed: ' + str(response.status_int))
        self.assertEqual(response.json[1]['name'], list_name_second,
                         'Creating shopping list failed: ' + str(response.status_int))
        first_id = str(response.json[0]['id'])

        # Check if shopping list is empty
        response = self.testapp.get(self.listURL+'/'+first_id, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Getting shopping list items failed: '+str(response.status_int))
        self.assertEqual(len(response.json), 0, 'Shopping list is not empty: ' + str(response.json))

        # Add product

        # Add some items
        first_desc = 'Tej'
        response = self.testapp.post(self.listURL+'/'+first_id, {'description': first_desc}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Adding items failed: '+str(response.status_int))
        response = self.testapp.post(self.listURL+'/'+first_id, {'description': first_desc}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Adding items failed: '+str(response.status_int))
        second_desc = 'Kenyer'
        response = self.testapp.post(self.listURL+'/'+first_id, {'description': second_desc, 'quantity': 3}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Adding items failed: '+str(response.status_int))

        # Adding to non-existing lists
        wrong_id = '0'
        response = self.testapp.post(self.listURL+'/'+wrong_id, {'description': first_desc}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Adding items failed: '+str(response.status_int))
        wrong_id = 'asd'
        response = self.testapp.post(self.listURL+'/'+wrong_id, {'description': first_desc}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Adding items failed: '+str(response.status_int))

        # Existing lists bad items
        response = self.testapp.post(self.listURL+'/'+first_id, {'description': first_desc, 'quantity': 'asd'}, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST, 'Adding items failed: '+str(response.status_int))

        # Check if shopping list contains added item(s)
        response = self.testapp.get(self.listURL+'/'+first_id, expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Getting shopping list items failed: '+str(response.status_int))
        self.assertEqual(len(response.json), 2, 'Shopping list should contain added item: ' + str(response.json))
        self.assertEqual(response.json[0]['description'], first_desc, 'Description of added item does not match: ' + str(response.json[0]['description']))
        self.assertEqual(int(response.json[0]['quantity']), 2, 'Quantity of added item does not match: ' + str(response.json[0]['quantity']))
        self.assertEqual(response.json[1]['description'], second_desc, 'Description of added item does not match: ' + str(response.json[1]['description']))
        self.assertEqual(int(response.json[1]['quantity']), 3, 'Quantity of added item does not match: ' + str(response.json[1]['quantity']))

        self.__logout__()

    def test_invalid_list_ids(self):
        """ Test invalid parameters as list_id """
        self.__login__()

        response = self.testapp.get(self.listURL+'/asd', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Shopping list queries should be served after authentication: ' + str(response.status_int))

        response = self.testapp.get(self.listURL+'/959894846485555648468', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Shopping list queries should be served after authentication: ' + str(response.status_int))

        response = self.testapp.get(self.listURL+'/15.25', expect_errors=True)
        self.assertEqual(response.status_int, constants.STATUS_BAD_REQUEST,
                         'Shopping list queries should be served after authentication: ' + str(response.status_int))

        self.__logout__()

    def __login__(self):
        email = 'james@bond.com'
        password = 'password'
        # 1. Register client
        response = UserUtil.register_user(self.testapp, email, password)
        self.assertEqual(response.status_int, constants.STATUS_OK,
                         'Register failed with correct credentials: ' + str(response.status_int))

        # 2. Verify
        response = UserUtil.verify_user(self.testapp, self.mail_stub, email)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Verification failed: ' + str(response.status_int))

    def __logout__(self):
        response = UserUtil.logout(self.testapp)
        self.assertEqual(response.status_int, constants.STATUS_OK, 'Logout failed: ' + str(response.status_int))
