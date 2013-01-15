# own files

# libraries
import webapp2
from django.core.validators import email_re

def valid_password(password):
	if password is None:
		return False
	if password == '':
		return False
	if len(password) < 8:
		return False
	return True

class UserRegisterHandler(webapp2.RequestHandler):
	def get(self):
		self.process()
	def post(self):
		self.process()
		
	def process(self):
		# Get and validate incoming parameters
		email = self.request.get('email')
		
		if not email_re.match(email):
			self.response.out.write('Invalid email<br>')
			self.error(400)
			return
			
		password = self.request.get('password')
		
		if not valid_password(password):
			self.response.out.write('Invalid arguments<br>')
			self.error(400)
			return
			
		# Calculate password hash
		
		# Create user object
		
		# Store credentials
		
		# Return
		self.response.out.write('Register request')
                 
