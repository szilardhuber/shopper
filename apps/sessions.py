# own files
from handlers import set_handlers
from sessionhandler import SessionHandler

# libraries
import webapp2
from webapp2 import Route

app = webapp2.WSGIApplication([
    	Route('/api/v<api_version>/sessions<:/?>', handler=SessionHandler, methods='POST'),
    	Route('/api/v<api_version>/sessions/<new:new><:/?>', handler=SessionHandler, methods='GET')
    ], debug=True)

set_handlers(app)
