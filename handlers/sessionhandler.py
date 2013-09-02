""" Contains ListHandler Class """
import logging

from handlers.basehandler import BaseHandler
from utilities import constants, CryptoUtil
from model import User
from gaesessions import get_current_session

class SessionHandler(BaseHandler):
    """ Handling requests for dealing with shopping lists """
#Public methods
    def get(self, api_version, new=None):
        """ get request handler """
        try:
            if int(api_version) < 2:
                raise ValueError('This method is only supported from api version 2.')

            email = self.request.get('email', None)
            if email is None or not User.isEmailValid(email):
                raise ValueError('Email parameter was not given.')

            if str(new) != 'new':
                raise ValueError('New parameter is not correct.')

            session = get_current_session()
            session[email] = CryptoUtil.getAccessToken()
            self.response.out.write('API: ' + str(api_version) + '<br>')
            self.response.out.write('Email: ' + email)
        except (ValueError) as exc:
            self.set_error(constants.STATUS_BAD_REQUEST)
            logging.error(exc.message)
            return

    def post(self,api_version):
        try:
            if int(api_version) < 2:
                raise ValueError('This method is only supported from api version 2.')
        except (ValueError) as exc:
            self.set_error(constants.STATUS_BAD_REQUEST)
            logging.error(exc.message)
            return

