# own files
from errorhandlers import set_handlers
from sessionhandler import SessionHandler

# libraries
import webapp2
from webapp2 import Route

app = webapp2.WSGIApplication([
    	Route('/api/v<api_version>/sessions<:/?>', handler=SessionHandler),
    	Route('/api/v<api_version>/sessions/<new:new>', handler=SessionHandler)
    ], debug=True)

set_handlers(app)
