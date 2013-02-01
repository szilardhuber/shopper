from gaesessions import get_current_session
from model.sessiondata import SessionData
from basehandler import APIView
from basehandler import WebView
from i18n_utils import LocalizedHandler

def viewneeded(func):
	def custom_call(*args, **kwargs):
		if args[len(args)-1].lower() == 'api':
			args[0].view = APIView.get_instance()
		else:
			args[0].view = WebView.get_instance()
		return func(*args, **kwargs)
	return custom_call

def usercallable(func):
	def custom_call(*args, **kwargs):
		session = get_current_session()
		args[0].user_email = session.get('email')
		return func(*args, **kwargs)
	return custom_call

def authenticate(func):
	def authenticate_and_call(handler, *args):
		session = get_current_session()
		sessionid = session.get('id')
		if not sessionid or sessionid == '' or not SessionData.isValidSession(sessionid):
			handler.set_error(401)
			return
		handler.user_email = session.get('email')
		return func(handler, *args)
	return authenticate_and_call
