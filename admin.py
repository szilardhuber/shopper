# own files
from adminproducthandler import AdminProductHandler

# libraries
import webapp2
                
app = webapp2.WSGIApplication([('/admin/Products', AdminProductHandler)
				],
                              debug=True)

                                                                                            
