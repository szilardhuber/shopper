# own files
from model import Action

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
		returnURL = self.request.get("returnURL");
		logging.info('User ' + guid + ' scanned code ' + barcode)
		action = Action()
		action.guid = guid
		action.barcode = barcode
		action.put()
		if returnURL == '':
			self.response.out.write('Guid: ' + guid + '<br>')
			self.response.out.write('Barcode: ' + barcode + '<br>')
		else:
			self.redirect(returnURL)
	

