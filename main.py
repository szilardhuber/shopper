# own files
from addproducthandler import AddProductHandler
from listproductshandler import ListProductsHandler

# libraries
import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('Service unavailable<br>')

app = webapp2.WSGIApplication([('/', MainPage),
				('/addproduct', AddProductHandler),
				('/AddProduct', AddProductHandler),
				('/ListProducts', ListProductsHandler),
				('/listproducts', ListProductsHandler),
				],
                              debug=True)

                                                                                            
