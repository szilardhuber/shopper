# own files
from userloginhandler import UserLoginHandler
from userregisterhandler import UserRegisterHandler

# libraries
import webapp2
                
app = webapp2.WSGIApplication([('/[uU]ser/[lL]ogin', UserLoginHandler),
				('/[uU]ser/[rR]egister', UserRegisterHandler)
				],
                              debug=True)
