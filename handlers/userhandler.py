""" Contains UserHandler class """
from model import User, LoginToken
from utilities import CryptoUtil, constants
from handlers.decorators import usercallable, viewneeded
from handlers.basehandler import BaseHandler

# another round with you track integration 14

# External libraries
from gaesessions import get_current_session
from base64 import b64encode
from google.appengine.api import mail
import logging
from datetime import datetime
from datetime import timedelta


class UserHandler(BaseHandler):

    """ Handling requests for dealing with shopping lists """

# Public methods
    @viewneeded
    @usercallable
    def get(self, command, api=''):
        """ GET request handler """
        if command.lower() == 'logout':
            self.__logout()
            return

        if api != '':
            self.set_error(constants.STATUS_BAD_REQUEST)
            return

        if command.lower() in ['login', 'register']:
            if self.user_email is not None:
                self.__display_form('alreadyloggedin.html')
            else:
                session = get_current_session()
                message = session.pop_quick(constants.VAR_NAME_ERRORMESSAGE)
                self.__display_form(command.lower() + '.html', message)
            return

        if command.lower() == 'verify':
            self.__verify()
            return

        self.set_error(constants.STATUS_NOT_FOUND)
        return

    @viewneeded
    def post(self, command, api=''):
        """ POST request handler """
        if api != '' and api.lower() != 'api':
            self.set_error(constants.STATUS_NOT_FOUND)
            return

        if command.lower() == 'login':
            self.__login()
            return

        if command.lower() == 'register':
            self.__register(api)
            return

        if command.lower() == 'verify' and api == '':
            email = self.request.get(constants.VAR_NAME_EMAIL)
            self.__send_verification(email)
            return

        self.set_error(constants.STATUS_NOT_FOUND)
        return

# Private methods
    def __send_verification(self, email):
        """ Send verification email to recipient """
        user = User.getUser(email.lower())
        if user is None or user.verified:
            self.set_error(constants.STATUS_BAD_REQUEST, message=None, url="/")
            return
        user.verificationCode = b64encode(CryptoUtil.get_verify_code(), "*$")
        template_values = {
            'user_email': self.user_email,
            'code': user.verificationCode,
            'url': constants.VERIFICATION_URL
        }
        template = self.jinja2_env.get_template('verificationemail.jinja')
        message = mail.EmailMessage()
        message.sender = constants.SENDER_ADDRESS
        message.to = user.email
        message.subject = 'Please verify your address'
        message.body = template.render(template_values)
        message.send()
        user.put()

    def __login(self):
        """ Validate incoming parameters and log in user if all is ok """
        # Validate email and get user from db
        email = self.request.get(constants.VAR_NAME_EMAIL)
        logging.info('User logging in: ' + str(email))
        if not User.isEmailValid(email) or not User.isAlreadyRegistered(email):
            logging.error('Email mismatched or not registered')
            self.set_error(constants.STATUS_BAD_REQUEST,
                           self.gettext('LOGIN_ERROR'), url=self.request.url)
            return
        user = User.getUser(email.lower())

        # Calculate password hash
        password = self.request.get(constants.VAR_NAME_PASSWORD)
        if not User.isPasswordValid(password):
            logging.error('Invalid password')
            self.set_error(constants.STATUS_BAD_REQUEST,
                           self.gettext('LOGIN_ERROR'), url=self.request.url)
            return
        key = CryptoUtil.getKey(password, user.salt)

        # Validate password
        if not user.password == key:
            logging.error('Incorrect password for email')
            self.set_error(constants.STATUS_BAD_REQUEST,
                           self.gettext('LOGIN_ERROR'), url=self.request.url)
            return

        # Check remember me
        remember_string = self.request.get('remember').lower()
        remember = remember_string != '' and remember_string != 'false'
        if remember:
            token_id = LoginToken.generate_id()
            token = LoginToken()
            token.tokenid = token_id
            token.ip = self.request.remote_addr
            token.user = email
            token.put()
            cookie_value = token.get_cookie_value()
            delta = timedelta(days=constants.PERSISTENT_LOGIN_LIFETIME_DAYS)
            self.response.set_cookie(constants.PERSISTENT_LOGIN_NAME,
                                     cookie_value,
                                     expires=datetime.utcnow() + delta,
                                     path="/", httponly=True, secure=True)

        # Log in user
        if user.verified:
            user.login(self.request.remote_addr)
            session = get_current_session()
            url = session.pop(constants.VAR_NAME_REDIRECT)
            if url is None:
                url = "/"
            self.ok(url)
        else:
            logging.error('User unverified')
            self.set_error(constants.STATUS_FORBIDDEN,
                           self.gettext('UNVERIFIED_PRE') +
                           ' <a href=\"/User/Verify">' +
                           self.gettext('UNVERIFIED_HERE') +
                           '</a> ' +
                           self.gettext('UNVERIFIED_POST'),
                           url=self.request.url)
            return

    def __logout(self):
        """ Do logout """
        if constants.PERSISTENT_LOGIN_NAME in self.request.cookies:
            token_cookie = self.request.cookies[constants.PERSISTENT_LOGIN_NAME]
            token = LoginToken.get_token_data(token_cookie)
            if token is not None:
                token.delete()
        self.response.delete_cookie(constants.PERSISTENT_LOGIN_NAME, '/')
        if self.user_email is not None and self.user_email != '':
            user = User.getUser(self.user_email.lower())
            if user is not None:
                user.logout()
        self.ok('/')

    def __register(self, api):
        """ Check incoming parameters and register user """
        # Validate email
        email = self.request.get(constants.VAR_NAME_EMAIL)
        logging.info('User registering: ' + str(email))
        if not User.isEmailValid(email) or User.isAlreadyRegistered(email):
            logging.error('Email mismatched or already registered')
            self.set_error(constants.STATUS_BAD_REQUEST,
                           self.gettext('REGISTER_ERROR'),
                           url=self.request.url)
            return

        # Validate password
        password = self.request.get(constants.VAR_NAME_PASSWORD)
        if not User.isPasswordValid(password):
            logging.error('Invalid password')
            self.set_error(constants.STATUS_BAD_REQUEST,
                           self.gettext('REGISTER_ERROR'),
                           url=self.request.url)
            return

        # Calculate password hash
        salt_and_key = CryptoUtil.get_salt_and_key(password)
        salt = salt_and_key[0]
        key = salt_and_key[1]

        # Create and store user object
        user = User(key_name=email)
        user.email = email.lower()
        user.salt = salt
        user.password = key
        user.verified = False
        user.put()

        # Send email for verification
        self.__send_verification(email)

        if api == '':
            # Display message
            template_values = {
                'message': self.gettext('PLEASE_CHECK_YOUR_EMAIL')
            }
            template = self.jinja2_env.get_template('staticmessage.html')
            self.response.out.write(template.render(template_values))

        self.ok()

    def __verify(self):
        """ Verify user who was assigned the code to """
        code = self.request.get('code')
        email = None
        error = False
        # resend if code is not given or in case of some error
        if code is not None and code != '':
            email = User.verify(code, self.request.remote_addr)
            if email is None:
                error = True

        if email is None:
            template_values = {
                'user_email': self.user_email,
                'error': error
            }
            template = self.jinja2_env.get_template('verification.html')
            self.response.out.write(template.render(template_values))

        # message
        template_values = {
            'user_email': self.user_email,
            'message': self.gettext('THANK_YOU')
        }
        template = self.jinja2_env.get_template('staticmessage.html')
        self.response.out.write(template.render(template_values))

    def __display_form(self, template, message=None):
        """ Display a the template """
        # page = memcache.get(str(language_code) + key, namespace='Pages')
        # if page is None:
        template_values = {
            'user_email': self.user_email,
            constants.VAR_NAME_ERRORMESSAGE: message
        }
        template = self.jinja2_env.get_template(template)
        page = template.render(template_values)
        # memcache.add(str(language_code) + key, page, namespace='Pages')
        self.response.out.write(page)
