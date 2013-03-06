from utilities import usercallable
from utilities import viewneeded
from basehandler import BaseHandler

class ListHandler(BaseHandler):
	def get(self, api=None, list_id=None):
		if api is not None:
			self.response.out.write('API!<br>')
			
		if list_id is None:
			self.response.out.write("List the URIs and perhaps other details of the collection's members. (Build server works like charm!)")
		else:
			self.response.out.write('Retrieve a representation of the addressed member of the collection, expressed in an appropriate Internet media type. #'+list_id)
			
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
		