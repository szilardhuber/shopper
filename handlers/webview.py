# own files
from utilities import constants

# builtins, libraries
import threading
from gaesessions import get_current_session

class WebView():
    instance = None
    instance_lock = threading.Lock()
    
    @staticmethod
    def get_instance():
        with WebView.instance_lock:
            if WebView.instance is None:
                WebView.instance = WebView()
        return WebView.instance
    
    def display_error(self, baseHandler, error, message=None, url=None):
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
        if url is not None:
            baseHandler.redirect(url)