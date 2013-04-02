from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler
from model import ShoppingList
from model import User
from model import ListItem
from utilities import constants
from utilities import authenticate
from utilities import usercallable

from model import Product
from utilities import to_JSON

import json
import logging

class ListHandler(BaseHandler):
	@viewneeded
	@authenticate
	def get(self, api=None, list_id=None):
		if list_id is None:
			# get all the lists of current user
			current_user = User.getUser(self.user_email)
			q = ShoppingList.all()
			q.ancestor(current_user)

			if api is not None:
				self.response.headers['Content-Type'] = 'application/json'
				all_lists = q.run()
				response_JSON = to_JSON(all_lists)
				self.response.out.write(response_JSON)
				return
			else:
				# get first list
				first_list = q.get()
				if first_list is None:
					first_list = self._create_list_('Shopping list')

				# navigate to it			
				newurl = '/Lists/' + str(first_list.key().id_or_name())
				self.redirect(newurl)
		else:
			try:
				current_user = User.getUser(self.user_email)
				current_list = ShoppingList.get_by_id(int(list_id), current_user)
				if current_list is None:
					raise ValueError

				if api is not None:
					self._api_display_list_(current_list)
				else:
					self._web_display_list_(current_list)
			except (TypeError, ValueError) as e: # filtering all non-integers in parameter
				logging.error(e)
				self.set_error(constants.STATUS_BAD_REQUEST, message=gettext("There's not such list, sorry."), url="/")
			
	@authenticate
	def put(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.set_error(constants.STATUS_BAD_REQUEST)
			return
		else:
			self.response.out.write("Replace the addressed member of the collection, or if it doesn't exist, create it. #"+list_id)

	@authenticate
	def post(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.response.out.write("Create a new entry in the collection. The new entry's URI is assigned automatically and is usually returned by the operation.")
			return
		else:
			# Add item to list
			try:
				current_user = User.getUser(self.user_email)
				current_list = ShoppingList.get_by_id(int(list_id), current_user)
				logging.info('Current list: ' + str(current_list))
				if current_list is None:
					raise ValueError
				
				current_list.add_item(self.request.get('description'), int(self.request.get('quantity', 1)))
				
				self.redirect('/Lists/'+str(list_id))

			except (TypeError, ValueError) as e: # filtering all non-integers in parameter
				logging.error('Exception: ' + str(e))
				self.set_error(constants.STATUS_BAD_REQUEST, message=gettext("There's not such list, sorry."), url="/")

	@authenticate
	def delete(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.response.out.write("Not supported here.")
			return
		else:
			self.response.out.write("Delete the addressed member of the collection. #")
			
	def _create_list_(self, list_name):
		current_user = User.getUser(self.user_email)
		new_list = ShoppingList(parent=current_user)
		new_list.name = 'Shopping list'
		new_list.put()
		return new_list
		
	def _api_display_list_(self, list_to_display):
		self.response.headers['Content-Type'] = 'application/json'
		response_JSON = to_JSON(list_to_display.get_items())
		self.response.out.write(response_JSON)
		
	def _web_display_list_(self, list_to_display):
		q = ListItem.all()
		q.ancestor(list_to_display)
		list_items = q.run()
		list_id = list_to_display.key().id_or_name()
		template = self.jinja2_env.get_template('shoppinglist.html')
		template_values = {
			'user_email' : self.user_email,
			'shopping_list' : list_to_display,
			'list_id' : list_id,
			'list_items' : list_items
		}
		self.response.out.write(template.render(template_values))
		
		