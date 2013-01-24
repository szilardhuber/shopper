# own files
from model import User

# libraries
from base64 import b64decode
import webapp2
from gaesessions import get_current_session

from i18n_utils import BaseHandler

class UserVerifyHandler(BaseHandler):
	def get(self):
		code = self.request.get('code')
		if code is None or code = '':
			pass # Please check your emails
		else:
			success = User.verify(code)
			if success:
				template = self.jinja2_env.get_template('verification.html')
				self.response.out.write(template.render())
			else:
				pass # Sorry this code has expired resend

	def post(self):
		pass # send out email
