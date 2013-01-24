# own files
from userloginhandler import UserLoginHandler
from userregisterhandler import UserRegisterHandler
from userlogouthandler import UserLogoutHandler

# libraries
import webapp2
                
app = webapp2.WSGIApplication([('/[uU]ser/[lL]ogin', UserLoginHandler),
				('/[uU]ser/[rR]egister', UserRegisterHandler),
				('/[uU]ser/[lL]ogout', UserLogoutHandler)
				],
                              debug=True)
