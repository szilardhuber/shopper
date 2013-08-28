import fix_path
from gaesessions import SessionMiddleware
from datetime import timedelta
from utilities import constants

from google.appengine.ext.appstats import recording

appstats_CALC_RPC_COSTS = True

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="28E42F03F4C8005CE5CAECF3571C006FEF3C1B78F7EC2FDA3E5FF69DA644D35C", lifetime=timedelta(hours=constants.SESSION_MAXIMUM_LIFETIME_HOURS))
    app = recording.appstats_wsgi_middleware(app)
    return app
