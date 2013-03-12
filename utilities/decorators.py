from gaesessions import get_current_session
from model.sessiondata import SessionData
from model import User
from apiview import APIView
from webview import WebView
from i18n_utils import LocalizedHandler
from utilities import constants

import logging
import datetime
from model.logintoken import LoginToken

def viewneeded(func):
	def custom_call(*args, **kwargs):
		args[0].view = WebView.get_instance()
		if len(args) > 1:
			if args[len(args)-1].lower() == 'api':
				args[0].view = APIView.get_instance()
		if len(kwargs) > 0:
			if 'api' in kwargs:
				args[0].view = APIView.get_instance()
		return func(*args, **kwargs)
	return custom_call

def usercallable(func):
	def custom_call(*args, **kwargs):
		session = get_current_session()
		args[0].user_email = session.get(constants.VAR_NAME_EMAIL)
		return func(*args, **kwargs)
	return custom_call

def authenticate(func):
	def success(handler):
		session = get_current_session()
		sessionid = session.get(constants.SESSION_ID)
		SessionData.getSession(sessionid).update_startdate()
		handler.user_email = session.get(constants.VAR_NAME_EMAIL)
		
	def error(handler):
		session = get_current_session()
		session.terminate()
		handler.set_error(constants.STATUS_UNAUTHORIZED)
		
	def authenticate_and_call(handler, *args, **kwargs):
		session = get_current_session()
		sessionid = session.get(constants.SESSION_ID)
		sessionData = SessionData.getSession(sessionid)
		if not sessionData or not sessionData.isValid():
			# if persistent id is given:
			if constants.PERSISTENT_LOGIN_NAME in handler.request.cookies:
				token_data = handler.request.cookies[constants.PERSISTENT_LOGIN_NAME]
				token = LoginToken.get(token_data)
				#	if persistent id is correct (email matches id following it): peform login 
				if token is not None:
					token.delete()
					token.tokenid = LoginToken.generateId()
					token.put()
					cookie_value = token.get_cookie_value()
					handler.response.set_cookie(constants.PERSISTENT_LOGIN_NAME, cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=constants.PERSISTENT_LOGIN_LIFETIME_DAYS), path="/", httponly=True, secure=True)
					user = User.getUser(token.user)
					user.login(handler.request.remote_addr)
					success(handler)
					logging.info('User logging in (with persistent token): ' + str(user.email))
				else:
					LoginToken.delete_user_tokens(token_data)
					error(handler)
					logging.info('Someone tried to authenticate with invalid token - email pair.')
					return
			else:			
				error(handler)
				return
		else:
			success(handler)
			logging.info('User logging in: ' + str(handler.user_email))
		return func(handler, *args, **kwargs)
	return authenticate_and_call
