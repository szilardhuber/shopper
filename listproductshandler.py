# own files
from model import Action
from utilities import authenticate

# libraries
from google.appengine.ext import db
import logging
import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.api import search

from i18n_utils import BaseHandler

class ListProductsHandler(BaseHandler):
	RESULTS_PER_PAGE = 10
	
	@authenticate
	def get(self):
		user_guid = self.request.get("guid");
		page = self.request.get("page");
		if page == '':
			page = 0
		else:
			page = int(page)
		
		logging.info('User (' + user_guid + ') listing items')
		actions = db.GqlQuery("SELECT * "
							"FROM Action "
							"WHERE guid = :1 "
							"ORDER BY date DESC LIMIT " + str(self.RESULTS_PER_PAGE) + ' OFFSET ' + str(page * self.RESULTS_PER_PAGE),
							user_guid)
		actionList = dict()
		for action in actions:
			query_obj = search.Query("barcode:"+action.barcode)
			results = search.Index(name='productindex').search(query=query_obj)
			if results.number_found > 0:
				actionList[action] = results.results[0].fields[0].value
			else:
				actionList[action] = ""

		#for barcode, productname in actionList.iteritems():
		#	self.response.out.write(barcode + ' ' + productname + '<br>')
			
		template_values = {
			'user_email' : self.user_email,
			'guid' : user_guid,
			'actions' : actions,
			'actionList': actionList,
			'page' : page,
			'lastPage' : 10
		}
		template = self.jinja2_env.get_template('productlist.html')
		self.response.out.write(template.render(template_values))                           
