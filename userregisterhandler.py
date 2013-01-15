# own files
from model import User
from utilities import CryptoUtil

# libraries
import webapp2

class UserRegisterHandler(webapp2.RequestHandler):
	def get(self):
		self.process()
	def post(self):
		self.process()
		
	def process(self):
		# Validate email
		email = self.request.get('email')
		if not User.isEmailValid(email):
			self.error(400)
			return
			
		# Validate password
		password = self.request.get('password')
		if not User.isPasswordValid(password):
			self.response.out.write('Invalid arguments<br>')
			self.error(400)
			return
			
		# Calculate password hash
		r = CryptoUtil.getKeyAndSalt(password)
		salt = r['salt']
		key = r['key']
		
		# Create user object
		user = User(key_name=email)
		user.email = email
		user.salt = salt
		user.password = key
		
		# Store credentials
		user.put()                 
