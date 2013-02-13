# own files
from userhandler import UserHandler

# libraries
import webapp2
                
app = webapp2.WSGIApplication([('/[uU]ser/(.*)/(.*)', UserHandler),
                ('/[uU]ser/(.*)', UserHandler)
				],
                              debug=True)
