# own files
from category import Category
from manufacturer import Manufacturer
from utilities import constants

# libraries
from google.appengine.ext import db
from google.appengine.api import memcache
import string
import logging
from argparse import Namespace

class Product(db.Model):
	barcode = db.StringProperty()
	description = db.StringProperty()
	category = db.ReferenceProperty(Category)
	manufacturer = db.ReferenceProperty(Manufacturer)
	name = db.StringProperty()
	non_allergic = db.StringListProperty()
	search_terms = db.StringListProperty()

	NAMESPACE='Product'
	
	@staticmethod
	def search(term):
		product_list = memcache.get(term, namespace=Product.NAMESPACE)
		if product_list is not None:
			return product_list
		product_list_query = Product.all()
		if term != 'all':
			product_list_query.filter('search_terms = ', term)
		product_list = product_list_query.fetch(1000)
		memcache.add(term, product_list, namespace=Product.NAMESPACE)
		return product_list
		
	
	def to_dict(self):
		ret = memcache.get(str(self.key().id_or_name()), namespace=Product.NAMESPACE)
		if ret is not None:
			return ret
		ret = dict([(p, unicode(getattr(self, p))) for p in self.properties() if p not in ['search_terms', 'category', 'manufacturer']])
		if self.category is not None:
			ret['category'] = self.category.to_dict()
		if self.manufacturer is not None:
			ret['manufacturer'] = self.manufacturer.to_dict()
		memcache.add(str(self.key().id_or_name()), ret, namespace=Product.NAMESPACE)
		return ret
	
	def set_name(self, name):
		search_terms = []
		
		words = name.split(' ')
		for word in words:
			term = ''
			for c in word:
				term = term + c
				search_terms.append(term.lower())

		self.search_terms = search_terms
		self.name = name 
		self.put()
	
	@staticmethod
	def is_in_db():
		q = Product.all()
		if q.get() == None:
			return False
		else:
			return True
		
	@staticmethod
	def fill_sample_data():
		tej_kat = Category()
		tej_kat.description = "Friss tej"
		tej_kat.put()
		
		mizo = Manufacturer()
		mizo.name = 'MiZo'
		mizo.put()
		
		milk = Product()
		milk.description = 'Fincsi tejcsi'
		milk.category = tej_kat
		milk.barcode = '5998200138614'
		milk.set_name('Mizo 1,5%-os zsirszegeny UHT tej 1 l')
		milk.manufacturer = mizo
		milk.non_allergic = []
		milk.put()
		
		zsepi_kat = Category()
		zsepi_kat.description = 'Zsebkendok'
		zsepi_kat.put()
		
		zewa = Manufacturer()
		zewa.name = 'Zewa'
		zewa.put()
		
		zsepi = Product()
		zsepi.description = 'Az orrodat is tiszticcsa'
		zsepi.category = zsepi_kat
		zsepi.barcode = '9011111535061'
		zsepi.set_name('Zewa Deluxe papir zsebkendo 90 db')
		zsepi.manufacturer = zewa
		zsepi.non_allergic = []
		zsepi.put()
	
	@staticmethod
	def add_some_more_data():	
		milk = Product()
		milk.description = 'Fincsi tejcsi 2'
		milk.barcode = '5998200450402'
		milk.set_name('Mizo 1,5% laktozmentes UHT tej 1 l')
		milk.non_allergic = []
		milk.put()
	

