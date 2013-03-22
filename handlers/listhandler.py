from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler
from model import ShoppingList
from model import User
from utilities import constants
from utilities import authenticate
from utilities import usercallable

import json
import logging

class ListHandler(BaseHandler):
	@viewneeded
	@authenticate
	def get(self, api=None, list_id=None):
		if api is not None:
			self.response.headers['Content-Type'] = 'application/json'
			
		if list_id is None:
			# get all the lists of current user
			current_user = User.getUser(self.user_email)
			q = ShoppingList.all()
			q.ancestor(current_user)

			if api is not None:
				all_lists = q.run()
				for shopping_list in all_lists:
					self.response.out.write(json.dumps(shopping_list.to_dict(), sort_keys=True, indent=4, separators=(',', ': ')))
				return
			else:
				# get first list
				first_list = q.get()
				if first_list is None:
					# if not found create it
					first_list = ShoppingList(parent=current_user)
					first_list.name = 'Shopping list'
					first_list.put()

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
					self.response.out.write(json.dumps(current_list.to_dict()))
				else:
					self.response.headers['Content-Type'] = 'application/json'
					self.response.out.write(json.dumps(current_list.to_dict(), sort_keys=True, indent=4, separators=(',', ': ')))
			except (TypeError, ValueError): # filtering all non-integers in parameter
				self.set_error(constants.STATUS_BAD_REQUEST, message=gettext("There's not such list, sorry."), url="/")
			
	def put(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.set_error(constants.STATUS_BAD_REQUEST)
			return
		else:
			self.response.out.write("Replace the addressed member of the collection, or if it doesn't exist, create it. #"+list_id)

	def post(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.response.out.write("Create a new entry in the collection. The new entry's URI is assigned automatically and is usually returned by the operation.")
			return
		else:
			self.response.out.write("Not supported here.")

	def delete(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.response.out.write("Not supported here.")
			return
		else:
			self.response.out.write("Delete the addressed member of the collection. #")
		