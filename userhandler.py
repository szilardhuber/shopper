from model.sessiondata import SessionData
from gaesessions import get_current_session

def perform_login(handler, email):
	sessionid = SessionData.generateId()
	sessionData = SessionData(key_name=sessionid)
	sessionData.sessionid = sessionid
	sessionData.email = email
	sessionData.ip = handler.request.remote_addr
	sessionData.put()
	session = get_current_session()
	session['id'] = sessionid
	session['email'] = email
#	redirectURL = session.pop_quick('url')
#	if redirectURL is not None:       
#		handler.redirect(redirectURL)
#	else:
#		handler.redirect('/')

def perform_logout(handler, email):
	session = get_current_session()
	sessionid = session.get('id')
	sessionData = SessionData.getSession(sessionid)
	if sessionData is not None:
		sessionData.delete()
	session['id'] = None
	session['email'] = None
#	handler.redirect('/')