""" Containst SessionCleanupHandler """
# own files
from gaesessions import delete_expired_sessions
from model.sessiondata import SessionData
from model import LoginToken

# libraries
import webapp2


class SessionCleanupHandler(webapp2.RequestHandler):
    """ Cleans up expired sessions and persistent tokens from memcache and datastore """

    def get(self):
        """ GET request handler """
        finished = False
        # while is needed as this geasessions function only deletes 500 sessions at a time
        while not finished:
            finished = delete_expired_sessions()
        SessionData.delete_expired_sessions()
        LoginToken.delete_expired_tokens()
