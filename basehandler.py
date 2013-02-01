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
    
    def display_error(self, baseHandler, error, message = None):
        baseHandler.error(error)
        
    def ok(self, baseHandler, url = None):
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
    
    def display_error(self, baseHandler, error, message = None):
        if error == 401:
            session = get_current_session()
            session['returnurl'] = baseHandler.request.url
            baseHandler.redirect('/User/Login')
        if error == 400:
            session = get_current_session()
            if message is not None:
                session['errormessage'] = message
            baseHandler.redirect(baseHandler.request.url)
            
    def ok(self, baseHandler, url = None):
        if url is not None:
            baseHandler.redirect(url)
            
 
class BaseHandler(LocalizedHandler):
    user_email = ""
    view = APIView()
    
    def set_error(self, error, message = None):
        self.view.display_error(self, error, message)
        
    def ok(self, url = None):
        self.view.ok(self, url)