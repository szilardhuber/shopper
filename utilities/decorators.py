from gaesessions import get_current_session
from model.sessiondata import SessionData
from i18n_utils import BaseHandler

from userhandler import perform_logout

def authenticate(func):
	def authenticate_and_call(handler):
		session = get_current_session()
		sessionid = session.get('id')
		if not sessionid or sessionid == '' or not SessionData.isValidSession(sessionid):
			perform_logout(handler, session.get('email'))
			handler.redirect('/User/Login')
		handler.user_email = session.get('email')
		return func(handler)
	return authenticate_and_call
