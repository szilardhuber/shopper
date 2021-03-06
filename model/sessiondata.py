""" Contains SessionData class """
from utilities import CryptoUtil
from utilities import constants

# libraries, builtins
from datetime import datetime, timedelta
from google.appengine.ext import db
from google.appengine.api import memcache


class SessionData(db.Model):

    '''
    Model object representing user sessions. The session is a limited time period until that we consider the user to be logged in.
    '''

    NAMESPACE = 'Session'

    email = db.EmailProperty()
    sessionid = db.ByteStringProperty()
    startdate = db.DateTimeProperty(auto_now_add=True)
    ip = db.StringProperty()

    @staticmethod
    def generate_id():
        '''
        Generates the sessionid user for authentication during the lifetime of the session. The output is hex_encoded
        '''
        return ''.join('%02x' % ord(byte) for byte in CryptoUtil.get_sessionId())

    @staticmethod
    def get_session(sessionid):
        '''
        Retrieves the session from the DB for the given id.
        :param sessionid:
        '''
        if sessionid is None:
            return None
        session = memcache.get(sessionid, namespace=SessionData.NAMESPACE)
        if session is not None:
            return session
        else:
            session = SessionData.get_by_key_name(sessionid, read_policy=db.STRONG_CONSISTENCY)
            if session is not None:
                memcache.add(sessionid, session, time=constants.SESSION_LIFETIME_IN_MEMCACHE, namespace=SessionData.NAMESPACE)
            return session

    def store(self):
        '''
        Store session data in memcache
        '''
        memcache.add(self.sessionid, self, time=constants.SESSION_LIFETIME_IN_MEMCACHE, namespace=SessionData.NAMESPACE)

    def delete(self):
        '''
        Override base function. Deletes value also from cache.
        '''
        memcache.delete(self.sessionid, namespace=SessionData.NAMESPACE)
        db.Model.delete(self)

    @staticmethod
    def delete_expired_sessions():
        '''
        Delete old sessions from datastore
        '''
        query = db.Query(SessionData)
        query.filter('startdate <', datetime.utcnow() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES))
        db.delete(query)

    def is_valid(self):
        '''
        Returns False if a session is too old
        '''
        return self.startdate > datetime.utcnow() - timedelta(minutes=constants.SESSION_LIFETIME_MINUTES)

    def update_startdate(self):
        '''
        We should update the startdate every time the user does something on the site
        '''
        self.startdate = datetime.utcnow()
        memcache.set(self.sessionid, self, time=36000, namespace=SessionData.NAMESPACE)
