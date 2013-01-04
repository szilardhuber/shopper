# own files

# libraries
import os
import webapp2
from google.appengine.api import search
from google.appengine.ext.webapp import template

def CreateDocument(productname, barcode):
	return search.Document(fields=[search.TextField(name='name', value=productname),
				search.TextField(name='barcode', value=barcode),
				])

class AdminProductHandler(webapp2.RequestHandler):
	def get(self):
		# if we have a search term, do the search and display results
		query = self.request.get('query')
		results = dict()
		if query != '':
			query_obj = search.Query(query)
			queryresults = search.Index(name='productindex').search(query=query_obj)
			# this hack is needed for django template to work
			for result in queryresults:
				results[result.fields[1].value] = result.fields[0].value + " (" + result.fields[1].value + ")"
		
		# if user clicked on new, display the edit form with empty fields
		product = False
		action = self.request.get('action')
		if action != '':
			product = True
		
		# if we have a barcode, get it and display edit form
		name = ''
		barcode = ''
		barcode = self.request.get('barcode')
		if barcode != '':
			product = True
			query_obj = search.Query('barcode:'+barcode)
			queryresults = search.Index(name='productindex').search(query=query_obj)
			if queryresults.number_found == 1:
				name = queryresults.results[0].fields[0].value

				
		template_values = {
			'results' : results,
			'barcode' : barcode,
			'name' : name,
			'product' : product
		}
                path = os.path.join(os.path.dirname(__file__), 'templates/productadmin.html')
                self.response.out.write(template.render(path, template_values))
        
	def post(self):
        	document = None
        	barcode = self.request.get('barcode')
        	name = self.request.get('name')
		query_obj = search.Query('barcode:'+barcode)
		queryresults = search.Index(name='productindex').search(query=query_obj)
		if queryresults.number_found == 1:
			document = queryresults.results[0]
			document.fields[0] = search.TextField(name='name', value=name)
		else:
			document = CreateDocument(name, barcode)
        	search.Index(name='productindex').put(document)
		self.redirect('')

