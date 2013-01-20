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
        redirectURL = session.pop('url')
        if redirectURL is not None:       
            handler.redirect(redirectURL)   
    