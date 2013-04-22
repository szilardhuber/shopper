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

    @classmethod
    def display_error(cls, base_handler, error, message=None, url=None):
        """ Display an error to the handled output """
        if error == constants.STATUS_UNAUTHORIZED:
            session = get_current_session()
            session[constants.VAR_NAME_REDIRECT] = base_handler.request.url
            base_handler.redirect(constants.LOGIN_PATH)
        if error == constants.STATUS_BAD_REQUEST:
            session = get_current_session()
            if message is not None:
                session[constants.VAR_NAME_ERRORMESSAGE] = message
            if url is not None:
                base_handler.redirect(url)
        if error == constants.STATUS_FORBIDDEN:
            session = get_current_session()
            if message is not None:
                session[constants.VAR_NAME_ERRORMESSAGE] = message
            base_handler.redirect(base_handler.request.url)

    @classmethod
    def ok(cls, base_handler, url=None):
        """ Redirect if needed """
        if url is not None:
            base_handler.redirect(url)
