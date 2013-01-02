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
		query = "WHERE guid = '" + str(guid) + "'"
		if barcode != '':
			query += " AND barcode = '" + str(barcode) + "'"
		returnURL = 'ListProducts'
		action = Action.gql(query)
		db.delete(action)
		if barcode != '':
			logging.info('User (' + guid + ') deleted product from list: ' + barcode)
		else:
			logging.info('User (' + guid + ') ordered all products from his list.')
		self.redirect("ListProducts?guid=%s" % str(guid))

