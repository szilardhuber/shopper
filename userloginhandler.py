# own files

# libraries
import webapp2

class UserLoginHandler(webapp2.RequestHandler):
	def get(self):
                self.response.out.write('Login request')
	def post(self):
                self.response.out.write('Login request')
                 
