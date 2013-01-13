# own files

# libraries
import webapp2

class UserRegisterHandler(webapp2.RequestHandler):
	def get(self):
                self.response.out.write('Register request')
	def post(self):
                self.response.out.write('Register request')
                 
