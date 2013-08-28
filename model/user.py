from sessiondata import SessionData
from utilities import constants
from logininfo import LoginInfo
from gaesessions import get_current_session

# libraries
from google.appengine.ext import db
from google.appengine.api import memcache
from django.core.validators import email_re
import re
import logging


class User(db.Model):

    '''
    Model object for representing users.
    '''
    email = db.EmailProperty()
    salt = db.ByteStringProperty()
    password = db.ByteStringProperty()
    registrationdate = db.DateTimeProperty(auto_now_add=True)

    NAMESPACE = 'User'

    @staticmethod
    def getUser(email):
        user = memcache.get(email, namespace=User.NAMESPACE)
        if user is not None:
            return user
        user = User.get_by_key_name(email, read_policy=db.STRONG_CONSISTENCY)
        memcache.add(email, user, namespace=User.NAMESPACE)
        return user

    @staticmethod
    def isAlreadyRegistered(email):
        current = User.getUser(email.lower())
        if current is None:
            return False
        else:
            return True

    @staticmethod
    def isEmailValid(email):
        '''
        Emails containing potentialy dangerous characters are considered to be invalid
        :param email:
        '''
        email_lower = email.lower()
        if not email_re.match(email_lower):
            return False
        if re.search(r'[^a-z0-9@._%+-]', email_lower) is not None:
            return False
        return True

    @staticmethod
    def isPasswordValid(password):
        '''
        At least 8 characters. No pontentialy dangerous ones.
        :param password:
        '''
        if password is None:
            return False
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return False
        if re.search(r'[;\'"<>]', password) is not None:
            return False
        return True

    def login(self, ip):
        sessionid = SessionData.generate_id()
        sessionData = SessionData(key_name=sessionid)
        sessionData.sessionid = sessionid
        sessionData.email = self.email
        sessionData.ip = ip
        sessionData.store()
        session = get_current_session()
        session[constants.SESSION_ID] = sessionid
        session[constants.VAR_NAME_EMAIL] = self.email
        LoginInfo.update(self)

    def logout(self):
        session = get_current_session()
        if session.get(constants.VAR_NAME_EMAIL) is None:
            return
        sessionid = session.get(constants.SESSION_ID)
        sessionData = SessionData.get_session(sessionid)
        if sessionData is not None:
            sessionData.delete()
        session.terminate()
        logging.info('User logged out: ' + self.email)
