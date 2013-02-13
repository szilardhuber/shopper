# folder handling
import fix_path

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

                                                                                            
