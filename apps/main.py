# folder handling
import os
from errorhandlers import set_handlers
from handlers import BaseHandler

# own files
from sessioncleanuphandler import SessionCleanupHandler

# libraries
import webapp2


class MainHandler(BaseHandler):

    def get(self):
		path = os.path.join(os.path.split(__file__)[0], '../static/templates/index.html')
		index_file = open(path)
		self.response.out.write(index_file.read())

app = webapp2.WSGIApplication([('/sessions', SessionCleanupHandler),
                                ('/', MainHandler)
                                ],debug=True)

set_handlers(app)
