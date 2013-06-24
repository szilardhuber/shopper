""" Contains LoginInfo model class """
from google.appengine.ext import db

#from datetime import datetime


class LoginInfo(db.Model):
    """ LoginInfo model class """
    lastlogindate = db.DateTimeProperty()
    logincount = db.IntegerProperty(0)

    @staticmethod
    def update(user):
        """ Write statistical data """
        return  # optimization / cost reduction
#        query = LoginInfo.all()
#        query.ancestor(user)
#        login_info = query.get()
#        if login_info is None:
#            login_info = LoginInfo(parent=user)
#        login_info.lastlogindate = datetime.utcnow()
#        if login_info.logincount is not None:
#            login_info.logincount += 1
#        else:
#            login_info.logincount = 1
#        login_info.put()
