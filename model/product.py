""" Contains Product class """

from utilities import to_JSON

# libraries
from google.appengine.ext import db
from google.appengine.api import memcache
import logging
from collections import defaultdict
import unicodedata
import json


class SearchHelper(db.Model):
    """ Helper class for searchin prefix """
    items = db.TextProperty(indexed=False)


class Product(db.Model):
    """ Model class for products """
    barcode = db.StringProperty()
    #description = db.StringProperty()
    #category = db.ReferenceProperty(Category)
    category = db.StringProperty()
    #manufacturer = db.ReferenceProperty(Manufacturer)
    name = db.StringProperty(indexed=True)
    #non_allergic = db.StringListProperty()
    #outer_id = db.StringProperty()
    #search_terms = db.StringListProperty()

    NAMESPACE = 'Product'

    @staticmethod
    def build_data():
        """ Build the data for searching if it's not in memcache """
        #all_products = Product.all().fetch(1500)
        all_products = db.Query(Product, projection=['name']).fetch(15000)
        ret = defaultdict(list)
        logging.info('Product count: ' + str(len(ret)))
        for product in all_products:
            for word in product.name.lower().split(' '):
                term = ''
                for char in word:
                    term = term + char
                    ret[term].append({'id': product.key().id_or_name(), 'name': product.name})
        for key, value in ret.iteritems():
            helper = SearchHelper(key_name=key)
            helper.items = to_JSON(value)
            helper.put()
        return ret

    @staticmethod
    def search(term):
        """ Return list of products that contain the given term in their name """
        term = unicodedata.normalize('NFKD', term).encode('ASCII', 'ignore')
        results = []
        for word in term.split(' '):
            if len(word) < 3:
                continue
            data = memcache.get(word, namespace=Product.NAMESPACE)
            if data is None:
                data = SearchHelper.get_by_key_name(word)
                if data is None:
                    return None
                memcache.add(term, data, namespace=Product.NAMESPACE)
            results.append(json.loads(data.items))
        ret = results[0]
        temp = []
        for result in results:
            temp = []
            for item in ret:
                if item in result:
                    temp.append(item)
            ret = temp
        return json.dumps(ret)

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
        self.search_terms = search_terms
        self.name = name
        return

        #words = name.split(' ')
        #for word in words:
        #    term = ''
        #    for char in word:
        #        term = term + char
        #        search_terms.append(term.lower())
        #self.search_terms = search_terms
        #self.name = name

    @staticmethod
    def is_in_db():
        """ Check if there is any product in the datastore """
        query = Product.all()
        if query.count() == 0:
            return False
        else:
            return True
