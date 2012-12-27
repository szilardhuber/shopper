# own files
from action import *

# libraries
import logging
import webapp2
from google.appengine.ext import webapp

class AddProductHandler(webapp2.RequestHandler):
	def post(self):
		self.process()
	def get(self):
		self.process()
	def process(self):
		guid = self.request.get("guid");
		barcode = self.request.get("barcode");
		logging.info('User ' + guid + ' scanned code ' + barcode)
		action = Action(user_key(guid))
		action.barcode = barcode
		action.put()
		self.response.out.write('Guid: ' + guid + '<br>')
		self.response.out.write('Barcode: ' + barcode + '<br>')
	

