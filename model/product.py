""" Contains Product class """
from model.category import Category
from model.manufacturer import Manufacturer

# libraries
from google.appengine.ext import db
from google.appengine.api import memcache
import logging

class Product(db.Model):
    """ Model class for products """
    barcode = db.StringProperty()
    description = db.StringProperty()
    category = db.ReferenceProperty(Category)
    manufacturer = db.ReferenceProperty(Manufacturer)
    name = db.StringProperty()
    non_allergic = db.StringListProperty()
    outer_id = db.StringProperty()
    search_terms = db.StringListProperty()

    NAMESPACE = 'Product'

    @staticmethod
    def search(term):
        """ Return list of products that contain the given term in their name """
        product_list = memcache.get(term, namespace=Product.NAMESPACE)
        product_list = None
        if product_list is not None:
            return product_list
        product_list_query = Product.all()
        terms = None
        if term != 'all':
            terms = term.split(' ')
            logging.info('Search terms: ' + str(terms))
            logging.info('DB term: ' + terms[0])
            product_list_query.filter('search_terms =', terms[0])
        product_list = product_list_query.fetch(1000)
        logging.info('Results count: ' + str(len(product_list)))
        if len(terms) > 1:
            for term in terms:
                if term != terms[0]:
                    product_list = [i for i in product_list if term in i.search_terms]
        memcache.add(term, product_list, namespace=Product.NAMESPACE)
        return product_list

    def to_dict(self):
        """ For JSON serialization """
        ret = memcache.get(str(self.key().id_or_name()), namespace=Product.NAMESPACE)
        if ret is not None:
            return ret
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties() if p not in [
                   'search_terms', 'category', 'manufacturer']])
        if self.category is not None:
            ret['category'] = self.category.to_dict()
        if self.manufacturer is not None:
            ret['manufacturer'] = self.manufacturer.to_dict()
        memcache.add(str(self.key().id_or_name()), ret, namespace=Product.NAMESPACE)
        return ret

    def set_name(self, name):
        """ When name is set, search terms should be updated
            This is a workaround for app engine search limitations.
        """
        search_terms = []

        words = name.split(' ')
        for word in words:
            term = ''
            for char in word:
                term = term + char
                search_terms.append(term.lower())

        self.search_terms = search_terms
        self.name = name

    @staticmethod
    def is_in_db():
        """ Check if there is any product in the datastore """
        query = Product.all()
        if query.count() == 0:
            return False
        else:
            return True

    @staticmethod
    def fill_sample_data():
        """ Add some initial data to datastore """
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
        """ More initial data """
        milk = Product()
        milk.description = 'Fincsi tejcsi 2'
        milk.barcode = '5998200450402'
        milk.set_name('Mizo 1,5% laktozmentes UHT tej 1 l')
        milk.non_allergic = []
        milk.put()
