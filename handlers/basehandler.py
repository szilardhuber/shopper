from apiview import APIView
from i18n_utils import LocalizedHandler
 
class BaseHandler(LocalizedHandler):
    user_email = ""
    view = APIView()
    
    def set_error(self, error, message=None, url=None):
        self.view.display_error(self, error, message, url)
        
    def ok(self, url=None):
        self.view.ok(self, url)
