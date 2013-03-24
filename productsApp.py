# own files
import fix_path
from producthandler import ProductHandler

# libraries
import webapp2
from webapp2 import Route
import logging
                
app = webapp2.WSGIApplication([
				Route('/<api:api>/v1/Products/', handler=ProductHandler),
				Route('/<api:api>/v1/products/', handler=ProductHandler),
				Route('/<api:api>/v1/Products', handler=ProductHandler),
				Route('/<api:api>/v1/products', handler=ProductHandler),
				Route('/<api:api>/v1/Products/<product_id>/', handler=ProductHandler),
				Route('/<api:api>/v1/Products/<product_id>/', handler=ProductHandler),
                Route('/Products/', handler=ProductHandler),
				Route('/products/', handler=ProductHandler),
				Route('/Products', handler=ProductHandler),
				Route('/products', handler=ProductHandler),
				Route('/Products/<product_id>/', handler=ProductHandler),
				Route('/products/<product_id>/', handler=ProductHandler)
				],
                              debug=True)

