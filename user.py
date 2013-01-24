# own files
from userloginhandler import UserLoginHandler
from userregisterhandler import UserRegisterHandler
from userlogouthandler import UserLogoutHandler
from userverifyhandler import UserVerifyHandler

# libraries
import webapp2
                
app = webapp2.WSGIApplication([('/[uU]ser/[lL]ogin', UserLoginHandler),
				('/[uU]ser/[rR]egister', UserRegisterHandler),
				('/[uU]ser/[lL]ogout', UserLogoutHandler),
				('/[uU]ser/[vV]erify', UserVerifyHandler)
				],
                              debug=True)
