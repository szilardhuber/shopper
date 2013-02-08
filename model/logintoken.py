# libraries
from google.appengine.ext import db
from utilities import CryptoUtil
from datetime import datetime, timedelta
from utilities import constants

import logging

class LoginToken(db.Model):
    user = db.EmailProperty()
    tokenid = db.ByteStringProperty()
    startdate = db.DateTimeProperty(auto_now_add=True)
    ip = db.StringProperty()

    @staticmethod
    def generateId():
        return ''.join('%02x' % ord(byte) for byte in CryptoUtil.getPersistentId())

    @staticmethod
    def getToken(tokenid, email):
        if tokenid is None:
            return None
        q = db.Query(LoginToken)
        q.filter('tokenid =', str(tokenid)) 
        q.filter('user =', email)
        return q.get()
    
    @staticmethod
    def delete_expired_tokens():
        q = db.Query(LoginToken)
        q.filter('startdate <', datetime.now() - timedelta(days=constants.PERSISTENT_LOGIN_LIFETIME_DAYS))
        db.delete(q)
        
    @staticmethod
    def split_token_string(token):
        parts = token.partition(';;')
        return parts[0],parts[2]
        
    @staticmethod
    def get(token):
        parts = LoginToken.split_token_string(token)
        if parts[0] == token:
            return None
        token_data = LoginToken.getToken(parts[1], parts[0])
        if token_data is None:
            return None
        if token_data.user != parts[0]:
            return None
        return token_data
    
    @staticmethod
    def delete_user_tokens(token):
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
        return self.user + ';;' + self.tokenid
        
