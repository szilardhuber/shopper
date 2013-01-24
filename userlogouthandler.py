# own files
from userhandler import perform_logout

# libraries
import webapp2
from gaesessions import get_current_session

from i18n_utils import BaseHandler

class UserLogoutHandler(BaseHandler):
	def get(self):
		session = get_current_session()
		if session.get('email') is not None:
			perform_logout(self, session.get('email'))

