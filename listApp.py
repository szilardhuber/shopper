# own files
import fix_path
from listhandler import ListHandler
from errorhandlers import set_handlers

# libraries
import webapp2
from webapp2 import Route

app = webapp2.WSGIApplication([
    Route('/<api:api>/v1/Lists/', handler=ListHandler),
    Route('/<api:api>/v1/lists/', handler=ListHandler),
    Route('/<api:api>/v1/Lists', handler=ListHandler), 
    Route('/<api:api>/v1/lists', handler=ListHandler),
    Route('/<api:api>/v1/Lists/<list_id>', handler=ListHandler),
    Route('/<api:api>/v1/lists/<list_id>', handler=ListHandler),
    Route('/<api:api>/v1/Lists/<list_id>/<item_id>',
          handler=ListHandler, methods='DELETE'),
    Route('/<api:api>/v1/lists/<list_id>/<item_id>',
          handler=ListHandler, methods='DELETE'),
    Route('/Lists/', handler=ListHandler, methods='GET'),
    Route('/lists/', handler=ListHandler, methods='GET'),
    Route('/Lists', handler=ListHandler, methods='GET'),
    Route('/lists', handler=ListHandler, methods='GET'),
    Route('/Lists/<list_id>', handler=ListHandler, methods='GET'),
    Route('/lists/<list_id>', handler=ListHandler, methods='GET')], debug=True)

set_handlers(app)
