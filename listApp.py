# own files
import fix_path
from listhandler import ListHandler
from errorhandlers import set_handlers

# libraries
import webapp2
from webapp2 import Route
import logging
                                
app = webapp2.WSGIApplication([
				Route('/<api:api>/v1/Lists/', handler=ListHandler),
				Route('/<api:api>/v1/lists/', handler=ListHandler),
				Route('/<api:api>/v1/Lists', handler=ListHandler),
				Route('/<api:api>/v1/lists', handler=ListHandler),
				Route('/<api:api>/v1/Lists/<list_id>', handler=ListHandler),
				Route('/<api:api>/v1/Lists/<list_id>', handler=ListHandler),
                Route('/Lists/', handler=ListHandler),
				Route('/lists/', handler=ListHandler),
				Route('/Lists', handler=ListHandler),
				Route('/lists', handler=ListHandler),
				Route('/Lists/<list_id>', handler=ListHandler),
				Route('/lists/<list_id>', handler=ListHandler)
				],
                              debug=True)

set_handlers(app)
