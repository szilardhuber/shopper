# own files
from handlers import AdminHandler
from handlers import AdminWorkerHandler

# libraries
import webapp2
from webapp2 import Route
                                
app = webapp2.WSGIApplication([
				Route('/admin', handler=AdminHandler),
                Route('/admin/worker', handler=AdminWorkerHandler)
				],
                              debug=True)

