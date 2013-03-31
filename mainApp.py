# folder handling
import fix_path
from errorhandlers import set_handlers

# own files
from listproductshandler import ListProductsHandler
from sessioncleanuphandler import SessionCleanupHandler

# libraries
import webapp2

app = webapp2.WSGIApplication([('/sessions', SessionCleanupHandler),
				('/(.*)', ListProductsHandler),
				('/ListProducts', ListProductsHandler),
				('/listproducts', ListProductsHandler)
				],debug=True)

set_handlers(app)                                                                                            