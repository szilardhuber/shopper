# own files
import fix_path
from listhandler import ListHandler

# libraries
import webapp2
from webapp2 import Route
import logging
                
def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)
    
def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!')
    response.set_status(500)
                
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

app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500