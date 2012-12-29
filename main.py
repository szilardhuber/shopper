# own files
from addproducthandler import AddProductHandler
from listproductshandler import ListProductsHandler

# libraries
import webapp2

import os
from google.appengine.ext.webapp import template

# this is only for temporary development purposes so that we can enter barcodes with iphone
class ScanHandler(webapp2.RequestHandler):
	def get(self):
		targetURL = '/AddProduct'
		user_guid = 123
                template_values = {
                	'guid' : user_guid,
                	'targetURL' : targetURL
                }
                path = os.path.join(os.path.dirname(__file__), 'templates/scan.html')
                self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([('/', ScanHandler),
				('/addproduct', AddProductHandler),
				('/AddProduct', AddProductHandler),
				('/ListProducts', ListProductsHandler),
				('/listproducts', ListProductsHandler),
				],
                              debug=True)

                                                                                            
