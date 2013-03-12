'''
    Login / Registration
'''

SESSION_LIFETIME_MINUTES = 1
SESSION_MAXIMUM_LIFETIME_HOURS = 12
PERSISTENT_LOGIN_LIFETIME_DAYS = 30
SENDER_ADDRESS = 'shopper@szilardhuber.appspotmail.com'
VERIFICATION_URL = 'https://szilardhuber.appspot.com/User/Verify?code='
SESSION_ID = "shopper_sid"
PERSISTENT_LOGIN_NAME = 'token'
VAR_NAME_EMAIL = 'email'
VAR_NAME_PASSWORD = 'password'
VAR_NAME_REDIRECT = 'returnurl'
VAR_NAME_ERRORMESSAGE = 'errormessage'
LOGIN_PATH = '/User/Login'

'''
	Shopping lists
'''
MAX_LISTS_COUNT = 10

'''
    Status codes
'''

STATUS_OK = 200 # The request has succeeded. 
STATUS_BAD_REQUEST = 400 # The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.
STATUS_UNAUTHORIZED = 401 # The request requires user authentication.
STATUS_FORBIDDEN = 403 # The server understood the request, but is refusing to fulfill it. Authorization will not help and the request SHOULD NOT be repeated
STATUS_NOT_FOUND = 404 # The server has not found anything matching the Request-URI.