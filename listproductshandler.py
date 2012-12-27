# own files
from action import *

# libraries
from google.appengine.ext import db
import logging
import webapp2

class ListProductsHandler(webapp2.RequestHandler):
	def get(self):
		user_guid = self.request.get("guid");
		logging.info('User listing items' + user_guid)
		actions = db.GqlQuery("SELECT * "
                            "FROM Action "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY date DESC LIMIT 10",
                            user_key(user_guid))
                for action in actions:
                	self.response.out.write('<b>%s</b><br>' % action.barcode)

