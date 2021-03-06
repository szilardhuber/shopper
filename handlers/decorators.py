""" Contains all decorator classes / functions """
from gaesessions import get_current_session
from model import SessionData
from model import User
from handlers.apiview import APIView
from handlers.webview import WebView
from utilities import constants

from datetime import datetime, timedelta
from model.logintoken import LoginToken


def viewneeded(func):
    """ Sets view member of the handler class to generate output """
    def custom_call(*args, **kwargs):
        """ The decorator itself """
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
    """ Sets the email of the current user to a member of the handler """
    def custom_call(*args, **kwargs):  # TODO SET BASED ON SESSIONID
        """ The decorator itself """
        session = get_current_session()
        args[0].user_email = session.get(constants.VAR_NAME_EMAIL)
        return func(*args, **kwargs)
    return custom_call


def authenticate(func):
    """ Performs session/token based authentication
        and redirects to login page if needed """
    def success(handler):
        """ Handle success """
        session = get_current_session()
        sessionid = session.get(constants.SESSION_ID)
        SessionData.get_session(sessionid).update_startdate()
        handler.user_email = session.get(constants.VAR_NAME_EMAIL)

    def error(handler):
        """ Handle error """
        session = get_current_session()
        session.terminate()
        handler.set_error(constants.STATUS_UNAUTHORIZED)

    def authenticate_and_call(handler, *args, **kwargs):
        """ The decorator itself """
        session = get_current_session()
        sessionid = session.get(constants.SESSION_ID)
        import logging
        logging.info('SessionID: ' + str(sessionid))
        session_data = SessionData.get_session(sessionid)
        if not session_data or not session_data.is_valid():
            # if persistent id is given:
            cookies = handler.request.cookies
            if constants.PERSISTENT_LOGIN_NAME in cookies:
                token_data = cookies[constants.PERSISTENT_LOGIN_NAME]
                token = LoginToken.get_token_data(token_data)
                #	if persistent id is correct (email matches id following it):
                #   peform login
                if token is not None:
                    token.delete()
                    token.tokenid = LoginToken.generate_id()
                    token.put()
                    cookie_value = token.get_cookie_value()
                    days = constants.PERSISTENT_LOGIN_LIFETIME_DAYS
                    expiration = datetime.utcnow() + timedelta(days=days)
                    handler.response.set_cookie(constants.PERSISTENT_LOGIN_NAME,
                                                cookie_value,
                                                expires=expiration,
                                                path="/",
                                                httponly=False,
                                                secure=True)
                    user = User.getUser(token.user)
                    user.login(handler.request.remote_addr)
                    success(handler)
                    logging.info('User logging in (with persistent token): ' +
                                 str(user.email))
                else:
                    LoginToken.delete_user_tokens(token_data)
                    error(handler)
                    logging.info('Someone tried to authenticate with \
                                    invalid token - email pair.')
                    return
            else:
                error(handler)
                return
        else:
            success(handler)
            logging.info('User logging in: ' + str(handler.user_email))
        return func(handler, *args, **kwargs)
    return authenticate_and_call
