# libraries
from google.appengine.ext import db

from datetime import datetime

class LoginInfo(db.Model):
	lastlogindate = db.DateTimeProperty()
	logincount = db.IntegerProperty(0)
	
	@staticmethod
	def update(user):
		return # optimization / cost reduction
		q = LoginInfo.all()
		q.ancestor(user)
		login_info = q.get()
		if login_info is None:
			login_info = LoginInfo(parent=user)
		login_info.lastlogindate = datetime.now()
		if login_info.logincount is not None:
			login_info.logincount += 1
		else:
			login_info.logincount = 1
		login_info.put()
		

