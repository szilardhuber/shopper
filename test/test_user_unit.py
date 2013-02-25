# own modules
from model import User

# builtins, libraries
import unittest


class UnitTests_User(unittest.TestCase):


    def testEmail(self):
        # Valid emails
        email = 'james@bond.com'
        self.assertTrue(User.isEmailValid(email), 'Misqualified valid email: ' + email)
        email = '123@ii.me'
        self.assertTrue(User.isEmailValid(email), 'Misqualified valid email: ' + email)
        email = 'dfssd32e23esd_%+3dw3d-sd-3-d--d-3-2-3d--s-d-sd-32-3@assssddasdwasdawdasdawdasdqw.info'
        self.assertTrue(User.isEmailValid(email), 'Misqualified valid email: ' + email)
        
        # Invalid emails
        email = 'ja\'mes@bond.com'
        self.assertFalse(User.isEmailValid(email), 'Misqualified invalid email: ' + email)
        email = 'ja\"mes@bond.com'
        self.assertFalse(User.isEmailValid(email), 'Misqualified invalid email: ' + email)
        email = ''
        self.assertFalse(User.isEmailValid(email), 'Misqualified invalid email: ' + email)
        email = ' '
        self.assertFalse(User.isEmailValid(email), 'Misqualified invalid email: ' + email)
        email = 'asd'
        self.assertFalse(User.isEmailValid(email), 'Misqualified invalid email: ' + email)
        email = "a'a@aisoft.hu"
        self.assertFalse(User.isEmailValid(email), 'Misqualified invalid email: ' + email)
    
    def testPassword(self):
        # Valid passwords
        password = '11111111'
        self.assertTrue(User.isPasswordValid(password), 'Misqualified valid password: ' + password)
        password = '111wr311111'
        self.assertTrue(User.isPasswordValid(password), 'Misqualified valid password: ' + password)
        password = 'asdasdawdas'
        self.assertTrue(User.isPasswordValid(password), 'Misqualified valid password: ' + password)
        
        # invalid passwords       
        password = '1234567'
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
        password = ''
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
        password = ' '
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
        password = '12 3 4567'
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
        password = 'asdasdasd;'
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
        password = 'asdasdasd\''
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
        password = 'asdasdasd"'
        self.assertFalse(User.isPasswordValid(password), 'Misqualified invalid password: ' + password)
                 