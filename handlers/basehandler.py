""" Base class for all handlers for making easier
    of separate display to web and api """
from handlers.apiview import APIView
from gettext import gettext
import webapp2

class BaseHandler(webapp2.RequestHandler):
    """ The base class itself """
    user_email = ""
    view = APIView()

    def set_error(self, error, message=None, url=None):
        """ Display and error message to the user and redirect if possible """
        self.view.display_error(self, error, message, url)

    def ok(self, url=None):
        """ Everything was ok, either redirect or do nothing """
        self.view.ok(self, url)

    @classmethod
    def gettext(cls, param):
        """ Dirty trick for fixing pylint report """
        return gettext(param)
