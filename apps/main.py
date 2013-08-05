# folder handling
from errorhandlers import set_handlers
from handlers import BaseHandler

# own files
from sessioncleanuphandler import SessionCleanupHandler

# libraries
import webapp2


class RedirectHandler(BaseHandler):

    def get(self):
        self.redirect('/Lists')

app = webapp2.WSGIApplication([('/sessions', SessionCleanupHandler),
                                ('/', RedirectHandler)
                                ],debug=True)

set_handlers(app)
