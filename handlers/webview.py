""" Contains WebView class """
from utilities import constants
import threading
from gaesessions import get_current_session


class WebView():
    """ Handles redirect and is smart when getting special error codes """
    instance = None
    instance_lock = threading.Lock()

    @staticmethod
    def get_instance():
        """ Singleton pattern """
        with WebView.instance_lock:
            if WebView.instance is None:
                WebView.instance = WebView()
        return WebView.instance

    def display_error(self, baseHandler, error, message=None, url=None):
        """ Display an error to the handled output """
        if error == constants.STATUS_UNAUTHORIZED:
            session = get_current_session()
            session[constants.VAR_NAME_REDIRECT] = baseHandler.request.url
            baseHandler.redirect(constants.LOGIN_PATH)
        if error == constants.STATUS_BAD_REQUEST:
            session = get_current_session()
            if message is not None:
                session[constants.VAR_NAME_ERRORMESSAGE] = message
            if url is not None:
                baseHandler.redirect(url)
        if error == constants.STATUS_FORBIDDEN:
            session = get_current_session()
            if message is not None:
                session[constants.VAR_NAME_ERRORMESSAGE] = message
            baseHandler.redirect(baseHandler.request.url)

    def ok(self, baseHandler, url=None):
        """ Redirect if needed """
        if url is not None:
            baseHandler.redirect(url)
