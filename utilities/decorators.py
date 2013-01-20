from gaesessions import get_current_session
from model.sessiondata import SessionData

def authenticate(func):
    def authenticate_and_call(*args, **kwargs):
        session = get_current_session()
        sessionid = session.get('id')
        if not sessionid or sessionid == '' or not SessionData.isValidSession(sessionid):
            session['url'] = args[0].request.url 
            args[0].redirect('/User/Login')
        return func(*args, **kwargs)
    return authenticate_and_call
