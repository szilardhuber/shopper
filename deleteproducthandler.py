# own files
from action import *

# libraries
from google.appengine.ext import db
import logging
import webapp2

class DeleteProductHandler(webapp2.RequestHandler):
	def get(self):
		guid = self.request.get("guid")
		barcode = self.request.get("barcode")
		returnURL = 'ListProducts'
		logging.info('User (' + guid + ') deleted product from list: ' + barcode)
		action = Action.gql("WHERE guid = :1 and barcode = :2", guid, barcode)
		db.delete(action)
		self.redirect("ListProducts?guid=%s" % str(guid))

