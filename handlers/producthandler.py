from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler
from model import ShoppingList
from model import User
from model import ListItem
from utilities import constants
from model import Product
from utilities import authenticate
from utilities import usercallable
from utilities import to_JSON

import logging

class ProductHandler(BaseHandler):
	@viewneeded
#	@authenticate
	def get(self, api=None, product_id=None):
		self.response.headers['Content-Type'] = 'application/json'

		if api is not None:
			self.response.headers['Content-Type'] = 'application/json'
			
		if product_id is None:
			q = self.request.get('q', '')
			product_list = Product.search(q)
			json_reponse = to_JSON(product_list)
			self.response.out.write(json_reponse)
		else:
			pass
			
	@authenticate
	def put(self, api=None, product_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if product_id is None:
			self.set_error(constants.STATUS_BAD_REQUEST)
			return
		else:
			pass

	@authenticate
	def post(self, api=None, product_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if product_id is None:
			return
		else:
			pass

	@authenticate
	def delete(self, api=None, product_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if product_id is None:
			self.response.out.write("Not supported here.")
			return
		else:
			self.response.out.write("Delete the addressed member of the collection. #")
		