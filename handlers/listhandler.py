from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler
from model import List
from model import User
from utilities import constants
from utilities import authenticate
from utilities import usercallable

import json

class ListHandler(BaseHandler):
	@authenticate
	def get(self, api=None, list_id=None):
		if api is not None:
			self.response.headers['Content-Type'] = 'application/json'
			
		if list_id is None:
			# get all the lists of current user
			current_user = User.getUser(self.user_email)
			q = List.all()
			q.ancestor(current_user)

			if api is not None:
				all_lists = q.run()
				for list in all_lists:
					self.response.out.write(json.dumps(list.to_dict(), sort_keys=True, indent=4, separators=(',', ': ')))
				return
			else:
				# for website just navigate to default list (and create it it not yet exist)
				# get first list
				first_list = q.get()
				if first_list is None:
					# if not found create it
					first_list = List(parent=current_user)
					first_list.name = 'Shopping list'
					first_list.put()

				# navigate to it			
				newurl = '/Lists/' + str(first_list.key().id_or_name())
				self.redirect(newurl)
		else:
			current_user = User.getUser(self.user_email)
			list = List.get_by_id(int(list_id), current_user)
			if list is None:
				pass # return error
			
			if api is not None:
				self.response.out.write(json.dumps(list.to_dict()))
			else:
				self.response.headers['Content-Type'] = 'application/json'
				self.response.out.write(json.dumps(list.to_dict(), sort_keys=True, indent=4, separators=(',', ': ')))
			
	def put(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.response.out.write("Not supported here.")
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
		