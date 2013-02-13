# own modules
from utilities import CryptoUtil
from utilities import constants

# libraries, builtins
from google.appengine.ext import db
from datetime import datetime, timedelta
import logging

class LoginToken(db.Model):
    '''
    Model object representing persistent login tokens. These tokens are used for the "remember me" functionality
    '''
    
    SEPARATOR = ';;'
    
    user = db.EmailProperty()
    tokenid = db.ByteStringProperty()
    startdate = db.DateTimeProperty(auto_now_add=True)
    ip = db.StringProperty()

    @staticmethod
    def generateId():
        '''
        Return the bytearray representing the token in an URL-friendly, hex-encoded way.
        '''
        return ''.join('%02x' % ord(byte) for byte in CryptoUtil.getPersistentId())

    @staticmethod
    def delete_expired_tokens():
        '''
        Deletes expired tokens from datastore
        '''
        q = db.Query(LoginToken)
        q.filter('startdate <', datetime.now() - timedelta(days=constants.PERSISTENT_LOGIN_LIFETIME_DAYS))
        db.delete(q)
        
    @staticmethod
    def split_token_string(token):
        '''
        Splits the token to email and value
        :param token: The token string in the following: email<LoginToken.SEPARATOR>token_hex_encoded
        '''
        parts = token.partition(LoginToken.SEPARATOR)
        return parts[0],parts[2]
        
    @staticmethod
    def get(token):
        '''
        Returns None for invalid input string or the token object for valid token string. Checks in the datastore
        if both the user and the token data are correct.
        :param token: The string format token
        '''
        if token is None:
            return None
        parts = LoginToken.split_token_string(token)
        if parts[0] == token:
            return None
        token_data = LoginToken.__get_token(parts[1], parts[0])
        if token_data is None:
            return None
        if token_data.user != parts[0]:
            return None
        return token_data
    
    @staticmethod
    def delete_user_tokens(token):
        '''
        Deletes all persistent tokens from the database for the user listed in the input string. This function should be called
        whenever someone uses an incorrect token.
        :param token:
        '''
        if token is None:
            return
        logging.critical('Trying to login with invalid token: ' + token)
        parts = LoginToken.split_token_string(token)
        if parts[0] == token:
            return
        q = db.Query(LoginToken)
        q.filter('user =', parts[0])
        db.delete(q)
    
    def get_cookie_value(self):
        '''
        Serialize the current object in the format that is used for storing in the cookie.
        '''
        return self.user + LoginToken.SEPARATOR + self.tokenid
    
    @staticmethod
    def __get_token(tokenid, email):
        '''
        Retrieves the token object from the datastore if both the email and the token data match
        :param tokenid:
        :param email:
        '''
        if tokenid is None or email is None:
            return None
        q = db.Query(LoginToken)
        q.filter('tokenid =', str(tokenid)) 
        q.filter('user =', email)
        return q.get()