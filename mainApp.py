# folder handling
import fix_path
from errorhandlers import set_handlers

# own files
from sessioncleanuphandler import SessionCleanupHandler

# libraries
import webapp2

class RedirectHandler(webapp2.RequestHandler):
	def get(self):
		self.redirect('/Lists', True)

app = webapp2.WSGIApplication([('/sessions', SessionCleanupHandler),
				('/', RedirectHandler)
				],debug=True)

set_handlers(app)                                                                                            