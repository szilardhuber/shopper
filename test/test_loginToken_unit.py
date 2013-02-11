from model import LoginToken

import unittest


class UnitTests_LoginToken(unittest.TestCase):
    def test(self):
        good_email = 'good@aisoft.hu'
        bad_email = 'bad@aisoft.hu'
        good_id = LoginToken.generateId()
        good_token = LoginToken()
        good_token.tokenid = good_id
        good_token.ip = '127.0.0.1'
        good_token.user = good_email
        good_token.put()
        bad_id = LoginToken.generateId()
        bad_token = LoginToken()
        bad_token.tokenid = bad_id
        bad_token.ip = '192.168.10.1'
        bad_token.user = bad_email
        bad_token.put()
        
        # Test for invalid input
        self.assertIsNone(LoginToken.get(''), 'We should not get a valid token for empty string')
        self.assertIsNone(LoginToken.get('someemail@aisoft.hu;;sometoken'))
        
        # Test for valid query
        cookie_value = good_email +';;' + str(good_id)
        queried_token = LoginToken.get(cookie_value)
        self.assertIsNotNone(queried_token, 'None returned for valid persistent token')
        self.assertEqual(good_token.user, queried_token.user, 'Valid persistent token not found.')
        self.assertEqual(good_token.tokenid, queried_token.tokenid, 'Valid persistent token not found.')
        
        # Test for hijacking
        bad_cookie_value = bad_email + ';;' + str(bad_id)
        queried_token = LoginToken.get(bad_cookie_value)
        self.assertIsNotNone(queried_token, 'None returned for valid persistent token')
        self.assertEqual(bad_token.user, queried_token.user, 'Valid persistent token not found.')
        self.assertEqual(bad_token.tokenid, queried_token.tokenid, 'Valid persistent token not found.')

        bad_cookie_value = bad_email + ';;' + str(good_id)
        queried_token = LoginToken.get(bad_cookie_value)
        self.assertIsNone(queried_token, 'Session hijacking danger')
        
        LoginToken.delete_user_tokens(bad_cookie_value)
        bad_cookie_value = bad_email + ';;' + str(bad_id)
        queried_token = LoginToken.get(bad_cookie_value)
        self.assertIsNone(queried_token, 'Session hijacking danger')
