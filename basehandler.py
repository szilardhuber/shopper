from utilities import constants

from gaesessions import get_current_session
from i18n_utils import LocalizedHandler
import threading

class APIView():    
    instance = None
    instance_lock = threading.Lock()
    
    @staticmethod
    def get_instance():
        with APIView.instance_lock:
            if APIView.instance is None:
                APIView.instance = APIView()
        return APIView.instance
    
    def display_error(self, baseHandler, error, message=None, url=None):
        baseHandler.error(error)
        
    def ok(self, baseHandler, url=None):
        pass

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
            
 
class BaseHandler(LocalizedHandler):
    user_email = ""
    view = APIView()
    
    def set_error(self, error, message=None, url=None):
        self.view.display_error(self, error, message, url)
        
    def ok(self, url=None):
        self.view.ok(self, url)
